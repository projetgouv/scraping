from utils import *
from constants import *

class UrlGenerator:
    def __init__(self,dataframe):
        self.dataframe = dataframe
        self.OBJECTIFS_URLS = []


    def generate_urls(self):
        for adresse in self.dataframe['search']:
# setting up the logging object
            logger = logging.getLogger('main')
            logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
    )

# we can change the logging level. Use logging.DEBUG if necesarry
            logger.setLevel(logging.DEBUG)



    # setting the chrome driver for selenium
            driver = webdriver.Chrome(service=Service(DRIVER_PATH))

    # opening the given URL
            logger.debug("Opening the given URL")
            driver.get(URL_PATH)

    # accepting the cookies
            logger.debug("Accepting the cookies")
            driver.find_element(By.CLASS_NAME,"lssxud").click()

    # writting the location in the search box
            time.sleep(2) 
            select_box = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
            select_box.send_keys(adresse)
            select_box.send_keys(Keys.ENTER)

    # waiting some random seconds
            time.sleep(random.uniform(4,6))

            page_url = driver.current_url
            self.OBJECTIFS_URLS.append(page_url)


            time.sleep(4)
            driver.quit()

    #print(page_url)
        return self.OBJECTIFS_URLS

#kash = UrlGenerator(dataframe = df, URL_PATH =  ma_variable, DRIVER_PATH=DRIVER_PATH)
#oli = kash.generate_urls()

