import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
import re

service = Service('D:/CarsBgWebScraper/chromedriver-win64/chromedriver.exe')
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=chrome_options)

with open('car_listings.csv', mode='r', encoding='utf-8', newline='') as infile:
    reader = csv.DictReader(infile)
    car_listings = list(reader)

with open('fullinfocars.csv', mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = reader.fieldnames + ['Additional Info']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for car in car_listings:
        link = car['Link']
        if link:
            driver.get(link)
            time.sleep(0.5)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            outer_text_copy_div = soup.find('div', class_='text-copy')
            if outer_text_copy_div:
                nested_text_copy_div = outer_text_copy_div.find('div', class_='text-copy')
                additional_info = nested_text_copy_div.text.strip() if nested_text_copy_div else 'N/A'
                additional_info = additional_info.replace('\n', ' ').replace('\r', ' ')
                additional_info = re.sub(r',\s+', ',', additional_info)
            else:
                additional_info = 'N/A'

            car['Additional Info'] = additional_info

        writer.writerow(car)

driver.quit()