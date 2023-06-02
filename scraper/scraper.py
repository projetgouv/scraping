import time
import random
import re
import os
import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

DRIVER_PATH = r'/home/oli/Projects/Google-review-scraper/chromedriver_linux64/chromedriver'
SAVING_PATH = '/Users/camille/repo/Hetic/projet_gouv/scraping/Data'

# declaring a list, that contains the urls which we want to be scraped
OBJECT_URLS = "https://www.google.com/maps/"
df_pe = pd.read_csv('/Users/camille/repo/Hetic/projet_gouv/scraping/pole_emploi.csv')

# setting up the logging object
logger = logging.getLogger('main')
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
)

# we can change the logging level. Use logging.DEBUG if necessary
logger.setLevel(logging.DEBUG)


def scrape_an_object(location):
    # setting the chrome driver for selenium
    driver = webdriver.Chrome(service=Service(DRIVER_PATH))

    # opening the given URL
    logger.debug("Opening the given URL")
    driver.get(OBJECT_URLS)

    # accepting the cookies
    logger.debug("Accepting the cookies")
    driver.find_element(By.CLASS_NAME, "lssxud").click()

    # waiting some random seconds
    time.sleep(random.uniform(4, 6))
    select_box = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
    select_box.send_keys(location)
    select_box.send_keys(Keys.ENTER)
    time.sleep(2)
    object_name = driver.find_element(
        By.CSS_SELECTOR,
        'h1.DUwDvf.fontHeadlineLarge'
    ).text
    logger.debug(f'Object_name OK : {object_name}')

    object_address = driver.find_element(
        By.CSS_SELECTOR,
        'div.Io6YTe.fontBodyMedium'
    ).text
    logger.debug(f'Object_address OK : {object_address}')

    # I use CSS selectors where I can because it's more robust than XPATH

    try:
        overall_rating = driver.find_element(
            By.CSS_SELECTOR,
            'div.F7nice.mmu3tf'
        ).text
        logger.debug(f'Overall_rating OK : {overall_rating}')

        review_number = driver.find_element(
            By.CSS_SELECTOR,
            'div.F7nice.mmu3tf'
        ).text.replace(' ', '')

        review_number = int(re.compile(r'\d+').findall(review_number)[-1])
        logger.debug(f'Review_number OK : {review_number}')

        # click to load further reviews
        driver.find_element(
            By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span'
        ).click()
        try:
            driver.find_element(
                By.CSS_SELECTOR,
                'button.Aq14fc'
            ).click()
        except NoSuchElementException:
            pass

        logger.debug('Clicked to load further reviews')

        time.sleep(random.uniform(0.1, 0.5))

        # find scroll layout
        scrollable_div = driver.find_element(
            By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'
        )

        logger.debug('Scroll div OK')

    except NoSuchElementException:

        logger.debug('Except branch')

        div_num_rating = driver.find_element(
            By.CSS_SELECTOR,
            'div.F7nice'
        ).text
        overall_rating = div_num_rating.split()[0]
        logger.debug(f'Overall_rating OK : {overall_rating}')

        review_number = int(div_num_rating.split()[1].replace('(', '').replace(')', ''))
        logger.debug(f'Review_number OK : {review_number}')

        # click on the review tab
        driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[1]').click()
        logger.debug('clicked to load further reviews')

        time.sleep(random.uniform(0.1, 0.5))

        # find scroll layout
        scrollable_div = driver.find_element(
            By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]'
        )
        logger.debug('Scroll div OK')

    time.sleep(random.uniform(2, 4))

    # scroll as many times as necessary to load all reviews
    while True:
        # Get the current height of the scrollable div
        current_height = driver.execute_script('return arguments[0].scrollHeight', scrollable_div)

        # Scroll to the bottom of the scrollable div
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        try:
            driver.find_element(
                By.CSS_SELECTOR,
                'button.w8nwRe.kyuRq'
            ).click()
        except NoSuchElementException:
            pass
        # Wait for some time to load more reviews
        time.sleep(random.uniform(1, 2))

        # Get the new height of the scrollable div after scrolling
        new_height = driver.execute_script('return arguments[0].scrollHeight', scrollable_div)

        # click on 'more' button if it appears
        try:
            driver.find_element(
                By.CSS_SELECTOR,
                'button.w8nwRe.kyuRq'
            ).click()
        except NoSuchElementException:
            pass

        # Check if the scrollable div height has changed
        if new_height == current_height:
            # No more reviews to load, exit the loop
            break

    # parse the HTML with a BeautifulSoup object
    response = BeautifulSoup(driver.page_source, 'html.parser')
    reviews_source = response.find_all('div', class_='jJc9Ad')
    logger.debug('Source code has been parsed!')

    # closing the browser
    driver.quit()

    # storing the data in a dict
    store_main_data = {'object_name': object_name,
                       'object_address': object_address,
                       'overall_rating': overall_rating,
                       'review_num': review_number,
                       'object_url': OBJECT_URLS}

    return store_main_data, reviews_source


def extract_reviews(reviews_source: list) -> list:
    """
    This method processes the input HTML code and returns a list containing the reviews.
    """
    review_list = []

    logger.debug('Starting to iterate through the reviews...')
    for review in reviews_source:
        # Extract the relevant information
        user = review.find('div', class_='d4r55').text.strip()
        date = review.find('span', class_='rsqaWe').text.strip()
        # Find rating elements and extract the ratings
        rate_elements = review.find_all('span', class_='kvMYJc')
        rate = int(rate_elements[0].get('aria-label').split()[0])

        review_text = review.find('span', class_='wiI7pd')
        review_text = '' if review_text is None else review_text.text

        review_list.append({
            'name': user,
            'date': date,
            'rate': rate,
            'review_text': review_text
        })

    return review_list


def main():
    # creating a list to store all objects scraped
    all_objects_data = []

    # iterating through each object URL in the list
    for location in df_pe['location']:
        # Get the corresponding object URL
        
        try:
            # Scrape data for the current location
            store_main_data, reviews_source = scrape_an_object(location)
        except:
            logger.debug(f'Error occurred for location: {location}. Moving to the next location.')
            continue

        review_list = extract_reviews(reviews_source)
        for review in review_list:
            review.update(store_main_data)  # Add the common data to each review
        all_objects_data.extend(review_list)
        logger.debug(f'{location} is done!')

        # Convert the scraped data to a DataFrame
        df = pd.DataFrame(all_objects_data)

        # Rearrange the columns
        df = df[['name', 'date', 'rate', 'review_text', 'object_name', 'object_address', 'overall_rating', 'review_num', 'object_url']]

        # Create the file path for saving the CSV file
        csv_file_location = os.path.join(SAVING_PATH, f'google_reviews_{location}.csv')

        # Write the DataFrame to a CSV file
        df.to_csv(csv_file_location, index=False)
        logger.debug(f"CSV file saved at: {csv_file_location}")

    # writing the complete dataframe to a single csv file
    all_csv_file_location = os.path.join(SAVING_PATH, 'google_reviews.csv')
    df.to_csv(all_csv_file_location, index=False)
    logger.debug(f"All objects CSV file saved at: {all_csv_file_location}")

if __name__ == '__main__':
    main()
