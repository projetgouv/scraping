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

"""Faire le scraping en POO prendre le code scraper"""