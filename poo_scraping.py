from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import dateparser

import time

class GoogleMaps:
    def __init__(self):
        # Remplacez le chemin vers le driver de votre navigateur
        driver_path = 'chromedriver'
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service)

    def search_location(self, location):
        # Ouvrir Google Maps
        self.driver.get('https://www.google.com/maps/')
        skip = self.driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button/span').click()
        search_box = self.driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
        search_box.send_keys(location)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
        search_box.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]/div[2]').click()
        time.sleep(2)
        text = search_box.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[9]/div[4]/div/div/div[4]/div[1]/span[2]')
        return text.text

# Exemple d'utilisation
maps = GoogleMaps()
location = 'Centre des impots de Paris 16'
print(location)
result = maps.search_location(location)
print(result)
