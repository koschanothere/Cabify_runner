import asyncio
import json
import random
import time
import logging
from copy import deepcopy
import scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s', encoding='utf-8')

# Load JSON data from files
with open(r'C:\Users\Kostya\Cabify_git\cabify\Analytics\origin_coords.json', encoding='utf-8') as f1:
    origin_coords_data = json.load(f1)

with open(r'C:\Users\Kostya\Cabify_git\cabify\Analytics\region_centroid.json', encoding='utf-8') as f2:
    region_centriods_data = json.load(f2)

class CoordinatesNotFoundError(Exception):
    pass

# Function to retrieve coordinates from region_centriods using OKATO_AO
def get_coordinates(okato_ao):
    for feature in region_centriods_data['features']:
        if int(feature['properties']['OKATO']) == okato_ao:
            return feature['geometry']['coordinates']
    raise CoordinatesNotFoundError(f"Coordinates not found for OKATO: {okato_ao}")

# Function to call the scraper with coordinates
async def call_scraper(driver, district_name, district_coords, region_coords, cycle):
    try:
        await scraper.runscraper(driver, district_name, district_coords, region_coords, cycle)
        logging.info(f"Scraper called successfully for {district_name}")
    except Exception as e:
        logging.error(f"Error calling scraper for {district_name}: {e}")

# Function to randomly shuffle origin coordinates and OKATO_AO
def shuffle_origin_coords():
    shuffled_coords = origin_coords_data['features'][:]
    random.shuffle(shuffled_coords)
    return shuffled_coords

def prep_coords(coords_list):
    try:
        coords_new = deepcopy(coords_list)
        coords_new.reverse()
        coordinates = ', '.join(map(str, coords_new))
        return coordinates
    except Exception as e:
        logging.error(f"Error in prep_coords with coords_list={coords_list}: {e}")
        return -1

# Function to run scraping process every hour
async def scrape_every_hour():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    shuffled_coords = shuffle_origin_coords()
    tasks = []
    cycle = 0
    for district in shuffled_coords:
        cycle += 1
        district_name = district['properties']['NAME']
        okato_ao = district['properties']['OKATO_AO']

        logging.info(f"Run {cycle}. Starting run for {district_name}. OKATO: {okato_ao}")

        district_coords = district['geometry']['coordinates']
        if district_coords is None:
            logging.error(f"District with none error: {district}")
        district_coords = prep_coords(district_coords)

        region_coords = get_coordinates(okato_ao)
        if region_coords is None:
            logging.error(f"OKATO with error: {okato_ao}")
        region_coords = prep_coords(region_coords)

        task = asyncio.create_task(call_scraper(driver, district_name, district_coords, region_coords, cycle))
        tasks.append(task)
    await asyncio.gather(*tasks)
    driver.quit()



time_begin = time.time()
asyncio.run(scrape_every_hour())
time_end = time.time()
print("Time to run: ", time_end - time_begin)