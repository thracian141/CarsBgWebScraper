import threading
import traceback
import signal
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import math
import concurrent.futures

stop_flag = threading.Event()

def signal_handler(sig, frame):
    print("Interrupt received, stopping...")
    stop_flag.set()

def generate_price_ranges(start, end, num_ranges):
    ranges = []
    step = (math.log(end) - math.log(start)) / num_ranges
    current = start
    for i in range(num_ranges):
        next_price = int(math.exp(math.log(current) + step))
        ranges.append((current, next_price))
        current = next_price + 1
    return ranges

def scrape_data(price_from, price_to, lock):
    if stop_flag.is_set():
        return
    print(f"Starting scrape for price range {price_from} to {price_to}")
    service = Service('./chromedriver-win64/chromedriver.exe')
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        url = f'https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&fuelId%5B%5D=1&fuelId%5B%5D=3&gearId=1&priceFrom={price_from}&priceTo={price_to}&conditions%5B%5D=4&conditions%5B%5D=1&yearFrom=2000&yearTo=2012&powerFrom=108&powerTo=252&doorId=2&e%5B%5D=9&e%5B%5D=26&steering_wheel=1'
        driver.get(url)

        unique_titles = set()

        previous_height = driver.execute_script("return document.body.scrollHeight")
        retries = 6
        while not stop_flag.is_set() and retries > 0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            try:
                WebDriverWait(driver, 35).until(
                    lambda d: d.execute_script("return document.body.scrollHeight") > previous_height
                )
                retries = 6  # Reset retries if successful
            except Exception as e:
                print(f"Timeout or error waiting for page to load: {e}")
                print(traceback.format_exc())
                retries -= 1
                if retries == 0:
                    break

            offer_items = driver.find_elements(By.CSS_SELECTOR, '.offer-item')
            for car_element in offer_items:
                if stop_flag.is_set():
                    break
                try:
                    primary_action = car_element.find_element(By.CSS_SELECTOR, '.mdc-card__primary-action')
                    d_grid = primary_action.find_element(By.CSS_SELECTOR, '.d-grid.no-decoration')

                    car_title = d_grid.find_element(By.CSS_SELECTOR, '.card__primary .card__title.mdc-typography--headline5').text
                    car_price = d_grid.find_element(By.CSS_SELECTOR, '.card__primary .card__title.price').text
                    vendor_info = primary_action.find_element(By.CSS_SELECTOR, '.card__footer').text
                    description = primary_action.find_element(By.CSS_SELECTOR, '.card__secondary.mdc-typography--body2').text

                    details = primary_action.find_element(By.CSS_SELECTOR, '.card__secondary.mdc-typography--body1.black').text

                    car_link = d_grid.get_attribute('href')

                    unique_identifier = (car_title, vendor_info)
                    if unique_identifier not in unique_titles:
                        unique_titles.add(unique_identifier)
                        with lock:
                            with open('1_listings.csv', mode='a', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                writer.writerow([car_title, car_price, details, vendor_info, description, car_link])
                except Exception as e:
                    print(f"Error extracting data: {e}")

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == previous_height:
                break

            previous_height = new_height
    finally:
        driver.quit()
        print(f"Finished scrape for price range {price_from} to {price_to}")

signal.signal(signal.SIGINT, signal_handler)

start_price_input = input("Enter the start price (default 2000): ")
end_price_input = input("Enter the end price (default 6000): ")

start_price = int(start_price_input) if start_price_input else 2000
end_price = int(end_price_input) if end_price_input else 6000

with open('1_listings.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Details', 'Vendor', 'Description', 'Link'])

price_ranges = generate_price_ranges(start_price, end_price, 6)

lock = threading.Lock()

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    futures = [executor.submit(scrape_data, price_from, price_to, lock) for price_from, price_to in price_ranges]
    try:
        for future in concurrent.futures.as_completed(futures):
            future.result()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, stopping...")
        stop_flag.set()
        for future in futures:
            future.cancel()

print("All scraping tasks completed.")