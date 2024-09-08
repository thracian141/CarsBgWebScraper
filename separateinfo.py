import csv
import re

# Regular expression to match engine volume with optional letters immediately after
engine_volume_pattern = re.compile(r'\b\d[.,]\d[a-zA-Z]*\b')

# Regular expressions to match year, fuel type, and mileage
year_pattern = re.compile(r'\b(19|20)\d{2}\b')
fuel_type_pattern = re.compile(r'Дизел|Бензин|Газ/Бензин')
mileage_pattern = re.compile(r'\d+\sкм\.?')

with open('car_listings.csv', mode='r', encoding='utf-8') as infile, open('separated_info.csv', mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow([header[0], 'Engine Volume', 'City', 'Year', 'Fuel Type', 'Mileage', 'Price', 'Vendor', 'Description', 'Link'])

    for row in reader:
        car_title = row[0]
        match = engine_volume_pattern.search(car_title)
        if match:
            engine_volume = match.group().replace(',', '.')
            car_title = engine_volume_pattern.sub('', car_title).strip()
            car_title = re.sub(r'\s+', ' ', car_title).strip()  # Remove extra spaces
        else:
            engine_volume = 'N/A'
        
        vendor_info = row[3]
        if ',' in vendor_info:
            parts = vendor_info.rsplit(',', 1)
            vendor_info = parts[0].strip()
            city = parts[1].strip()
        else:
            city = 'N/A'
        
        # Extract year, fuel type, and mileage using regex
        details = row[2]
        year_match = year_pattern.search(details)
        fuel_type_match = fuel_type_pattern.search(details)
        mileage_match = mileage_pattern.search(details)

        year = year_match.group() if year_match else 'N/A'
        fuel_type = fuel_type_match.group() if fuel_type_match else 'N/A'
        mileage = mileage_match.group() if mileage_match else 'N/A'

        # Handle price conversion if it includes "EUR"
        price = row[1]
        if 'EUR' in price:
            price_value = float(price.replace('EUR', '').replace(',', '').strip())
            price_value_bgn = price_value * 1.956
            price = f"{price_value_bgn:.2f} лв."
        else:
            price = price.replace(',', '').strip()

        # Handle missing description gracefully
        description = row[4] if len(row) > 4 else 'N/A'

        # Include the link in the output
        link = row[5] if len(row) > 5 else 'N/A'

        writer.writerow([car_title, engine_volume, city, year, fuel_type, mileage, price, vendor_info, description, link])