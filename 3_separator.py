import csv
import re

engine_volume_pattern = re.compile(r'\b\d[.,]\d[a-zA-Z]*\b')
year_pattern = re.compile(r'\b(19|20)\d{2}\b')
fuel_type_pattern = re.compile(r'Дизел|Бензин|Газ/Бензин')
mileage_pattern = re.compile(r'\d+\sкм\.?')
manufacture_date_pattern = re.compile(r'^[A-Za-zА-Яа-яЁё\s]*\d{4}$')
shape_pattern = re.compile(r'^[A-Za-zА-Яа-яЁё\s]+$')
euro_mark_pattern = re.compile(r'^(EURO|euro|Euro)\s?[1-6]$')
color_pattern = re.compile(r'^[A-Za-zА-Яа-яЁё\s]+$')

with open('2_fullinfo.csv', mode='r', encoding='utf-8') as infile, open('3_separated.csv', mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow([header[0], 'Engine Volume', 'City', 'Year', 'Fuel Type', 'Mileage', 'Price', 'Vendor', 'Description', 'Link', 'Shape', 'HorsePower', 'EuroMark', 'Color'])

    for row in reader:
        car_title = row[0]
        match = engine_volume_pattern.search(car_title)
        if match:
            engine_volume = match.group().replace(',', '.')
            car_title = engine_volume_pattern.sub('', car_title).strip()
            car_title = re.sub(r'\s+', ' ', car_title).strip()
        else:
            engine_volume = 'N/A'
        
        vendor_info = row[3]
        if ',' in vendor_info:
            parts = vendor_info.rsplit(',', 1)
            vendor_info = parts[0].strip()
            city = parts[1].strip()
        else:
            city = 'N/A'
        
        details = row[2]
        year_match = year_pattern.search(details)
        fuel_type_match = fuel_type_pattern.search(details)
        mileage_match = mileage_pattern.search(details)

        year = year_match.group() if year_match else 'N/A'
        fuel_type = fuel_type_match.group() if fuel_type_match else 'N/A'
        mileage = mileage_match.group() if mileage_match else 'N/A'

        price = row[1]
        if 'EUR' in price:
            price_value = float(price.replace('EUR', '').replace(',', '').strip())
            price_value_bgn = price_value * 1.956
            price = f"{price_value_bgn:.2f} лв."
        else:
            price = price.replace(',', '').strip()

        description = row[4] if len(row) > 4 else 'N/A'
        link = row[5] if len(row) > 5 else 'N/A'

        additional_info = row[6] if len(row) > 6 else 'N/A'
        if additional_info != 'N/A':
            additional_info = additional_info.replace('\n', ' ').replace('\r', ' ')
            parts = additional_info.split(',')

            manufacture_date = shape = horse_power = euro_mark = volume = color = 'N/A'
            
            if len(parts) > 0:
                manufacture_date = parts[0].strip()
                manufacture_date_match = manufacture_date_pattern.match(manufacture_date)
                if manufacture_date_match:
                    manufacture_date = manufacture_date[-4:]
                else:
                    manufacture_date = 'N/A'
            
            for part in parts[1:-1]:
                part = part.strip()
                if shape == 'N/A' and shape_pattern.match(part):
                    shape = part
                elif horse_power == 'N/A' and re.match(r'^\d+к\.с\.$', part):
                    horse_power = part
                elif euro_mark == 'N/A' and euro_mark_pattern.match(part):
                    euro_mark = part
                elif volume == 'N/A' and re.match(r'^\d{4}см3$', part):
                    volume_match = re.match(r'(\d{4})см3', part)
                    if volume_match:
                        volume = f"{int(volume_match.group(1)) / 1000:.1f}"

            # Check the last part for color
            last_part = parts[-1].strip()
            if color_pattern.match(last_part):
                color = last_part

        # Determine the final year value
        year = year if year != 'N/A' else manufacture_date
        engine_volume = engine_volume if engine_volume != 'N/A' else volume

        writer.writerow([car_title, engine_volume, city, year, fuel_type, mileage, price, vendor_info, description, link, shape, horse_power, euro_mark, color])