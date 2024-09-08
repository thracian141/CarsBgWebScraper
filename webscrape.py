from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import csv

# Initialize the WebDriver
service = Service('D:/CarsBgWebScraper/chromedriver-win64/chromedriver.exe')
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get('https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&fuelId%5B%5D=1&fuelId%5B%5D=3&gearId=1&last=3&priceFrom=2000&priceTo=6000&conditions%5B%5D=4&conditions%5B%5D=1&yearFrom=2000&powerFrom=90&doorId=2&steering_wheel=1')

time.sleep(0.5)

# Open CSV file and write header
with open('car_listings.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Vendor', 'Description'])

    # Set to track unique car titles
    unique_titles = set()

    previous_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)
        new_height = driver.execute_script("return document.body.scrollHeight")

        offer_items = driver.find_elements(By.CSS_SELECTOR, '.offer-item')
        for car_element in offer_items:
            try:
                primary_action = car_element.find_element(By.CSS_SELECTOR, '.mdc-card__primary-action')
                d_grid = primary_action.find_element(By.CSS_SELECTOR, '.d-grid.no-decoration')

                car_title = d_grid.find_element(By.CSS_SELECTOR, '.card__primary .card__title.mdc-typography--headline5').text
                car_price = d_grid.find_element(By.CSS_SELECTOR, '.card__primary .card__title.price').text
                vendor_info = primary_action.find_element(By.CSS_SELECTOR, '.card__footer').text
                description = primary_action.find_element(By.CSS_SELECTOR, '.card__secondary.mdc-typography--body2').text

                # Check for duplicates using both title and vendor
                unique_identifier = (car_title, vendor_info)
                if unique_identifier not in unique_titles:
                    unique_titles.add(unique_identifier)
                    writer.writerow([car_title, car_price, vendor_info, description])
            except Exception as e:
                print(f"Error extracting data: {e}")

        if new_height == previous_height:
            break

        previous_height = new_height

driver.quit()