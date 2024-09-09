import csv
import re

# Define the functions for each criterion
def price_points(price):
    if price == 0:
        return 0
    if price < 2000:
        return 10  
    elif 2000 <= price <= 3000:
        return 10 + 10 * (price - 2000) / (3000 - 2000) 
    elif 3000 < price <= 6000:
        return 20 * (6000 - price) / (6000 - 3000)  
    else:
        return 0  

def city_points(city):
    if 'София' in city:
        return 8
    elif 'Пловдив' in city:
        return 10
    elif 'Варна' in city:
        return 6
    elif 'Враца' in city:
        return 1
    elif 'Бургас' in city:
        return 7
    elif 'Стара Загора' in city:
        return 8
    elif 'Монтана' in city:
        return 0
    elif 'Плевен' in city:
        return 2
    elif 'Пазарджик' in city:
        return 9
    elif 'Смолян' in city:
        return 4
    elif 'Кърджали' in city:
        return 3
    elif 'Русе' in city:
        return 2
    elif 'Сливен' in city:
        return 4
    elif 'Хасково' in city:
        return 4
    elif 'Ямбол' in city:
        return 4
    elif 'Велико Търново' in city:
        return 3
    elif 'Габрово' in city:
        return 3
    elif 'Добрич' in city:
        return 1
    elif 'Казанлък' in city:
        return 5
    elif 'Видин' in city:
        return 0
    elif 'Кюстендил' in city:
        return 5
    elif 'Благоевград' in city:
        return 6
    elif 'Асеновград' in city:
        return 10
    else:
        return 0
    
def volume_points(volume):
    if volume < 1.2:
        return 0
    elif 1.2 <= volume <= 2.0:
        return 10 * (volume - 1.2) / (2.0 - 1.2) 
    elif 2.0 < volume <= 3.0:
        return 10 * (3.0 - volume) / (3.0 - 2.0) 
    else:
        return 0
    
def hp_points(hp):
    match hp:
        case 'N/A':
            return 0
        case _ if hp < 90:
            return 0
        case _ if hp >= 90 and hp < 100 :
            return 2
        case _ if hp >= 100 and hp < 120:
            return 6
        case _ if hp >= 120 and hp < 140:
            return 8
        case _ if hp >= 140 and hp < 160:
            return 10
        case _ if hp >= 160 and hp < 180:
            return 8
        case _ if hp >= 180 and hp < 200:
            return 6
        case _ if hp >= 200:
            return 0
  
def brand_points(brand):
    if 'volkswagen' in brand:
        return 8
    elif 'vw' in brand:
        return 8
    elif 'opel' in brand:
        return 5
    elif 'renault' in brand:
        return 5
    elif 'skoda' in brand:
        return 5
    elif 'ford' in brand:
        return 4
    elif 'peugeot' in brand:
        return 6
    elif 'citroen' in brand:
        return 5
    elif 'fiat' in brand:
        return 3
    elif 'toyota' in brand:
        return 10
    elif 'mazda' in brand:
        return 7
    elif 'honda' in brand:
        return 9
    elif 'hyundai' in brand:
        return 8
    elif 'nissan' in brand:
        return 6
    elif 'kia' in brand:
        return 5
    elif 'chevrolet' in brand:
        return 4
    elif 'seat' in brand:
        return 4
    elif 'mercedes' in brand:
        return 2
    elif 'bmw' in brand:
        return -10
    elif 'volvo' in brand:
        return 9
    elif 'alfa romeo' in brand:
        return 6
    elif 'dacia' in brand:
        return 1
    elif 'suzuki' in brand:
        return 5
    elif 'jaguar' in brand:
        return 0
    elif 'lancia' in brand:
        return 6
    else:
        return 0

def mileage_points(mileage):
    if mileage < 30000:
        return 0
    elif mileage == 'N/A':
        return 0
    elif mileage == '':
        return 0
    elif mileage > 320000:
        return 0
    elif mileage < 100000:
        return 10
    else:
        return 10 * (320000 - mileage) / (320000 - 100000)

def year_of_manufacture_points(year):
    if year <= 2000:
        return 0
    elif year > 2010:
        return 10
    elif year > 2000 and year <= 2010:
        return year - 2000
    else:
        return 0

def fuel_type_points(fuel_type):
    if 'Дизел' in fuel_type:
        return -5
    elif 'Бензин' in fuel_type:
        return 0
    elif 'Газ/Бензин' in fuel_type:
        return 5
    else:
        return 0
    
def shape_points(shape):
    match shape:
        case 'Седан':
            return 10
        case 'Хечбек':
            return 8
        case 'Комби':
            return 6
        case 'Купе':
            return 4
        case 'Кабрио':
            return 2
        case 'Джип':
            return 0
        case 'Миниван':
            return 0
        case 'Пикап':
            return 0
        case 'Ван':
            return 0
        case 'Друг':
            return 0
        case 'N/A':
            return 0
        case _:
            return 0
        
def euro_mark_points(euro_mark):
    match euro_mark:
        case 'Евро 6':
            return 10
        case 'Евро 5':
            return 10
        case 'Евро 4':
            return 9
        case 'Евро 3':
            return 5.5
        case 'Евро 2':
            return 3
        case 'Евро 1':
            return 0
        case 'N/A':
            return 0
        case _:
            return 0

def calculate_points(car):
    points = 0
    
    try:
        price = float(re.sub(r'[^\d.]', '', car['Price']))
    except (ValueError, KeyError):
        price = 0
    points += price_points(price)
    
    points += city_points(car.get('City', ''))
    
    try:
        engine_volume = float(car['Engine Volume'].replace(',', '.'))
    except (ValueError, KeyError):
        engine_volume = 0
    points += volume_points(engine_volume)
    
    brand = car.get('Title', '').lower()
    points += brand_points(brand)
    
    try:
        mileage = int(re.sub(r'[^\d]', '', car['Mileage']))
    except (ValueError, KeyError):
        mileage = 0
    points += mileage_points(mileage)
    
    try:
        year = int(car['Year of Manufacture'])
    except (ValueError, KeyError):
        year = 0
    points += year_of_manufacture_points(year)
    
    points += fuel_type_points(car.get('Fuel Type', ''))
    
    if 'астно лице' not in car.get('Vendor', ''):
        points -= 3
    
    return round(points, 2)

# Read the CSV file and rank the cars
with open('separated_info.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    cars = list(reader)

    for car in cars:
        car['Points'] = calculate_points(car)

    # Sort cars by points in descending order
    ranked_cars = sorted(cars, key=lambda x: x['Points'], reverse=True)

# Write the ranked cars to a new CSV file
with open('ranked_car_listings.csv', mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = reader.fieldnames + ['Points']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(ranked_cars)