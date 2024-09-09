import csv
import re
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Rank car listings')
    parser.add_argument('--opt_price', type=float, help='Optimal price for full points (default: 3000)')
    return parser.parse_args()

args = parse_arguments()

if args.opt_price is None:
    while True:
        try:
            args.opt_price = float(input("Enter the optimal price for full points (default 3000): ") or 3000)
            break
        except ValueError:
            print("Please enter a valid number.")

# Define the functions for each criterion
def price_points(price, opt_price):
    match price:
        case _ if price == 2000:
            return 10
        case _ if 2000 <= price <= opt_price:
            return 10 + 10 * (price - 2000) / (opt_price - 2000) 
        case _ if opt_price < price <= 6000:
            return 20 * (6000 - price) / (6000 - opt_price)  
        case _:
            return 0  

def city_points(city):
    match city:
        case _ if 'София' in city:
            return 8
        case _ if 'Пловдив' in city:
            return 10
        case _ if 'Варна' in city:
            return 6
        case _ if 'Враца' in city:
            return 1
        case _ if 'Бургас' in city:
            return 7
        case _ if 'Стара Загора' in city:
            return 8
        case _ if 'Монтана' in city:
            return 0
        case _ if 'Плевен' in city:
            return 2
        case _ if 'Пазарджик' in city:
            return 9
        case _ if 'Смолян' in city:
            return 4
        case _ if 'Кърджали' in city:
            return 3
        case _ if 'Русе' in city:
            return 2
        case _ if 'Сливен' in city:
            return 4
        case _ if 'Хасково' in city:
            return 4
        case _ if 'Ямбол' in city:
            return 4
        case _ if 'Велико Търново' in city:
            return 3
        case _ if 'Габрово' in city:
            return 3
        case _ if 'Добрич' in city:
            return 1
        case _ if 'Казанлък' in city:
            return 5
        case _ if 'Видин' in city:
            return 0
        case _ if 'Кюстендил' in city:
            return 5
        case _ if 'Благоевград' in city:
            return 6
        case _ if 'Асеновград' in city:
            return 10
        case _:
            return 0
    
def volume_points(volume):
    match volume:
        case _ if volume < 1.2:
            return 0
        case _ if 1.2 <= volume <= 2.0:
            return 10 * (volume - 1.2) / (2.0 - 1.2) 
        case _ if 2.0 < volume <= 3.0:
            return 10 * (3.0 - volume) / (3.0 - 2.0) 
        case _:
            return 0
    
def hp_points(hp):
    match hp:   
        case _ if hp < 85:
            return 0 
        case _ if 85 <= hp <= 135:
            return 10 * (hp - 85) / (135 - 85) 
        case _ if 135 < hp <= 300:
            return 10 * (300 - hp) / (300 - 135)  
        case _:
            return 0 
  
def brand_points(brand):
    match brand:
        case _ if 'volkswagen' in brand:
            return 8
        case _ if 'vw' in brand:
            return 8
        case _ if 'opel' in brand:
            return 5
        case _ if 'renault' in brand:
            return 5
        case _ if 'skoda' in brand:
            return 5
        case _ if 'ford' in brand:
            return 4
        case _ if 'peugeot' in brand:
            return 6
        case _ if 'citroen' in brand:
            return 5
        case _ if 'fiat' in brand:
            return 3
        case _ if 'toyota' in brand:
            return 10
        case _ if 'mazda' in brand:
            return 7
        case _ if 'honda' in brand:
            return 9
        case _ if 'hyundai' in brand:
            return 8
        case _ if 'nissan' in brand:
            return 6
        case _ if 'kia' in brand:
            return 5
        case _ if 'chevrolet' in brand:
            return 4
        case _ if 'seat' in brand:
            return 4
        case _ if 'mercedes' in brand:
            return 2
        case _ if 'bmw' in brand:
            return -10
        case _ if 'volvo' in brand:
            return 9
        case _ if 'alfa romeo' in brand:
            return 6
        case _ if 'dacia' in brand:
            return 1
        case _ if 'suzuki' in brand:
            return 5
        case _ if 'jaguar' in brand:
            return 0
        case _ if 'lancia' in brand:
            return 6
        case _:
            return 0


def mileage_points(mileage):    
    match mileage:
        case _ if mileage < 30000:
            return 0
        case _ if mileage == 'N/A':
            return 0
        case _ if mileage == '':
            return 0
        case _ if mileage > 320000:
            return 0
        case _ if mileage < 100000:
            return 10
        case _:
            return 10 * (320000 - mileage) / (320000 - 100000)

def year_of_manufacture_points(year):
    match year:
        case _ if year <= 2000:
            return 0
        case _ if year > 2010:
            return 10
        case _ if year > 2000 and year <= 2010:
            return year - 2000
        case _:
            return 0

def fuel_type_points(fuel_type):
    match fuel_type:
        case _ if 'Дизел' in fuel_type:
            return -5
        case _ if 'Бензин' in fuel_type:
            return 0
        case _ if 'Газ/Бензин' in fuel_type:
            return 5
        case _:
            return 0

def calculate_points(car):
    points = 0
    
    # Extract and format the values before passing them to the respective functions
    try:
        price = float(re.sub(r'[^\d.]', '', car['Price']))
    except (ValueError, KeyError):
        price = 0
    points += price_points(price, args.opt_price)
    
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

# Define a custom BMW car dictionary
custom_car = {
    'Title': 'BMW',
    'Price': '5,000 EUR',
    'City': 'София',
    'Engine Volume': '2.0',
    'Mileage': '150000 км.',
    'Year of Manufacture': '2015',
    'Fuel Type': 'Бензин',
    'Vendor': 'частно лице',
    'Link': 'https://www.cars.bg/offer/66db38487017b7d9ed017bd2'
}

# Calculate points for the custom car
custom_car_points = calculate_points(custom_car)

# Print the result
print(f"Custom BMW car points: {custom_car_points}")

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