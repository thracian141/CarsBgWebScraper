price_ranges = [(2000, 2666), (2667, 3333), (3334, 4000), (4001, 4666), (4667, 5333), (5334, 6000)]
for price_from, price_to in price_ranges:
  url = f'https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&fuelId%5B%5D=1&fuelId%5B%5D=3&gearId=1&priceFrom={price_from}&priceTo={price_to}&conditions%5B%5D=4&conditions%5B%5D=1&yearFrom=2000&yearTo=2012&powerFrom=108&powerTo=252&doorId=2&e%5B%5D=9&e%5B%5D=26&steering_wheel=1'
  print(f"URL: {url}")

