import csv
import re

# Regular expression to match engine volume with optional letters immediately after
engine_volume_pattern = re.compile(r'\b\d[.,]\d[a-zA-Z]*\b')

with open('car_listings.csv', mode='r', encoding='utf-8') as infile, open('separated_info.csv', mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow([header[0], 'Engine Volume', 'City'] + header[1:])

    for row in reader:
        car_title = row[0]
        match = engine_volume_pattern.search(car_title)
        if match:
            engine_volume = match.group().replace(',', '.')
            car_title = engine_volume_pattern.sub('', car_title).strip()
            car_title = re.sub(r'\s+', ' ', car_title).strip()  # Remove extra spaces
        else:
            engine_volume = 'N/A'
        
        vendor_info = row[2]
        if ',' in vendor_info:
            parts = vendor_info.rsplit(',', 1)
            vendor_info = parts[0].strip()
            city = parts[1].strip()
        else:
            city = 'N/A'
        
        writer.writerow([car_title, engine_volume, city] + row[1:2] + [vendor_info] + row[3:])