import asyncio
import json
import logging
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os


# Configure logging
log_file_path = os.path.join(os.getenv('GITHUB_WORKSPACE'), 'scraper.log')
logging.basicConfig(filename='scraper.logs', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s', encoding='utf-8')

async def runscraper(driver, name="Test", pointA="55.85995110810542, 37.56275798748232", pointB="55.88762047186569, 37.451297918193326", cycle=0, retries=3):
    log = {
        "Run": cycle,
        "District": name,
        "Point A": pointA,
        "Point B": pointB
    }
    logging.info(f"Starting scraper for: {log}")

    try:
        #driver.get("http://127.0.0.1:5500")
        driver.get("http://cabift.great-site.net")

        wait_for_map = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds

        origin_input = wait_for_map.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Откуда']")))
        origin_input.clear()
        origin_input.send_keys(pointA)
        
        destination_input = wait_for_map.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Куда']")))
        destination_input.clear()
        destination_input.send_keys(pointB)

        sleep(0.1)

        try:
            # Check for the error element
            error_element = driver.find_elements(By.CLASS_NAME, "ymaps-2-1-79-route-panel-error__text")
            if error_element:
                raise Exception("Map error detected")
        except NoSuchElementException:
            # Error element not found, proceed normally
            pass

        wait = WebDriverWait(driver, 5)  # Maximum wait time of 5 seconds
        dynamic_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ymaps-2-1-79-route-content")))
        
        duration_element = dynamic_element.find_element(By.CLASS_NAME, "ymaps-2-1-79-route-content__title")
        duration_text, length_text = duration_element.text.split(',')[0].strip().split('&')[0], duration_element.text.split(' ')[2].split('&')[0]

        price_element = driver.find_element(By.CLASS_NAME, "ymaps-2-1-79-route-content__description")
        price_text = price_element.text.split(' ')[1]

        data = {
            "District": name,
            "Price": price_text,
            "Duration": duration_text,
            "Length": length_text
        }

        write_to_json(data)
        logging.info(f"Data for {name}: {data}")

    except (Exception, TimeoutException) as e:
        logging.error(f"An error occurred for {name}: {e}")
        if retries > 0:
            logging.info(f"Retrying for {name}, attempts left: {retries}")
            await runscraper(driver, name, pointA, pointB, cycle, retries - 1)
        else:
            logging.error(f"Max retries reached for {name}. Aborting.")


def write_to_json(data, filename='data.json'):
    now = datetime.now()
    date_time = now.strftime("%d/%m %H:%M")

    entry = {
        "Date": date_time.split()[0],
        "Time": date_time.split()[1],
        "District": data["District"],
        "Value": {
            "Price": data["Price"],
            "Duration": data["Duration"],
            "Length": data["Length"]
        }
    }

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        json_data = []

    json_data.append(entry)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    
    logging.info(f"Entry added to {filename}: {entry}")

# Run the scraper
# asyncio.run(runscraper())
