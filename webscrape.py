from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

chrome_options = Options()
chrome_options.add_argument("--headless")

service = Service('D:/CarsBgWebScraper/chromedriver-win64/chromedriver.exe')

driver = webdriver.Chrome(service=service, options=chrome_options)

url = 'https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&fuelId%5B%5D=1&fuelId%5B%5D=3&gearId=1&last=3&priceFrom=2000&priceTo=6000&conditions%5B%5D=4&conditions%5B%5D=1&yearFrom=2000&powerFrom=90&doorId=2&steering_wheel=1'
driver.get(url)

time.sleep(3)

car_elements = driver.find_elements(By.CSS_SELECTOR, '.offer-item')[:20]
print(f"Found {len(car_elements)} car elements")

car_data_list = []

for car_element in car_elements:
    try:
        primary_action = car_element.find_element(By.CSS_SELECTOR, '.mdc-card__primary-action')
        d_grid = primary_action.find_element(By.CSS_SELECTOR, '.d-grid.no-decoration')

        # Extract the car title from the correct h5 element
        car_title = d_grid.find_element(By.CSS_SELECTOR, '.card__primary .card__title.mdc-typography--headline5').text
        print("Car title element found:", car_title)

        # Extract the car price from the correct h6 element
        car_price = d_grid.find_element(By.CSS_SELECTOR, '.card__primary .card__title.price').text
        print("Car price element found:", car_price)

        # Extract the vendor information from the correct div element
        vendor_info = primary_action.find_element(By.CSS_SELECTOR, '.card__footer').text
        print("Vendor information found:", vendor_info)

        # Extract the description from the correct div element
     