import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import concurrent.futures
import threading

def process_chunk(chunk, writer_lock, stop_event):
    service = Service('./chromedriver-win64/chromedriver.exe')
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    for car in chunk:
        if stop_event.is_set():
            break

        link = car['Link']
        if link:
            driver.get(link)
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'text-copy'))
                )
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                outer_text_copy_div = soup.find('div', class_='text-copy')
                if outer_text_copy_div:
                    nested_text_copy_div = outer_text_copy_div.find('div', class_='text-copy')
                    additional_info = nested_text_copy_div.text.strip() if nested_text_copy_div else 'N/A'
                    additional_info = additional_info.replace('\n', ' ').replace('\r', ' ')
                    additional_info = re.sub(r',\s+', ',', additional_info)
                else:
                    additional_info = 'N/A'
            except:
                additional_info = 'N/A'

            car['Additional Info'] = additional_info

        with writer_lock:
            writer.writerow(car)

    driver.quit()

service = Service('./chromedriver-win64/chromedriver.exe')
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=chrome_options)

with open('1_listings.csv', mode='r', encoding='utf-8', newline='') as infile:
    reader = csv.DictReader(infile)
    car_listings = list(reader)

chunk_size = len(car_listings) // 6
chunks = [car_listings[i:i + chunk_size] for i in range(0, len(car_listings), chunk_size)]

with open('2_fullinfo.csv', mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = reader.fieldnames + ['Additional Info']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    writer_lock = threading.Lock()
    stop_event = threading.Event()

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(process_chunk, chunk, writer_lock, stop_event) for chunk in chunks]
            concurrent.futures.wait(futures)
    except KeyboardInterrupt:
        stop_event.set()
        for future in futures:
            future.cancel()
        print("Processing interrupted by user.")