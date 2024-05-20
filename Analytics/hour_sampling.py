import asyncio
import json
import random
import time
import logging
import hashlib
import pandas as pd
from datetime import datetime
from copy import deepcopy
import scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

features = []
with open('scraper.logs', 'w'):
    pass

# Configure logging
logging.basicConfig(filename='scraper.logs', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s', encoding='utf-8')

# Load JSON data from files
with open(r'Analytics\origin_coords.json', encoding='utf-8') as f1:
    origin_coords_data = json.load(f1)

with open(r'Analytics\region_centroid.json', encoding='utf-8') as f2:
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
        data = await scraper.runscraper(driver, district_name, district_coords, region_coords, cycle)
        preprocess_data_and_append(data)
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

        f"Run {cycle}. Starting run for {district_name}. OKATO: {okato_ao}"

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


def feature_hashing_district(district, num_buckets):
    return int(hashlib.sha256(district.encode('utf-8')).hexdigest(), 16) % num_buckets

def preprocess_data_and_append(entry):
    current_year = datetime.now().year  # Get the current year
    
    # Calculate current date and time
    current_date = datetime.now().strftime('%d/%m/%Y')
    current_time = datetime.now().strftime('%H:%M')
    
    # Extract date and time features
    date_parts = current_date.split('/')
    day_of_week = pd.to_datetime(current_date, format='%d/%m/%Y').dayofweek
    month = int(date_parts[1])
    hour = int(current_time.split(':')[0])

    # Feature hashing for district names
    district_hash = feature_hashing_district(entry["District"], num_buckets=1000)
    
    # Extract numerical values
    try:
        price = float(entry["Price"])
        duration = int(entry["Duration"].split()[0])  # Extract only the numerical part
        length = float(entry["Length"].replace(',', '.'))  # Handle decimal comma
    except ValueError as e:
        logging.error(f"Error processing entry: {e}")
        return None
    
    # Append to global features list
    global features
    features.append({
        "DayOfWeek": day_of_week,
        "Month": month,
        "Hour": hour,
        "District": district_hash,
        "Price": price,
        "Duration": duration,
        "Length": length
    })
    
    logging.info("Preprocessing completed for entry: %s", entry)


def dump_to_json(df, filename='data.json'):
    try:
        # Convert DataFrame to list of dictionaries
        features_list = df.to_dict(orient='records')
        
        with open(filename, 'a+') as f:
            if not os.path.isfile(filename) and os.path.getsize(filename) > 0:
                # If file is empty, write data without appending
                json.dump(features_list, f)
            else:
                # If file is not empty, append a comma and then the data
                f.seek(0, os.SEEK_END)
                f.seek(f.tell() - 1, os.SEEK_SET)
                f.truncate()  # Remove the trailing ']'
                f.write(',')  # Add a comma
                f.write(json.dumps(features_list)[1:])  # Write the data without the leading '['
            logging.info("Features dumped to %s", filename)
    except Exception as e:
        logging.error("Error dumping features to JSON file: %s", e)

time_begin = time.time()
asyncio.run(scrape_every_hour())
df = pd.DataFrame(features)
dump_to_json(df)
time_end = time.time()
print("Time to run: ", time_end - time_begin)
