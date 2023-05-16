from utils import *
from constants import *


class MyScraper :
    def __init__(self, object_url : str):
        self.object_url = object_url
        self.reviews_source = []
        self.store_main_data = {}
        self.review_list = []
        self.setfunction()

    def setfunction(self) :

        # setting up the logging object
        logger = logging.getLogger('main')
        logging.basicConfig(
            format='[%(asctime)s] [%(levelname)s] - %(message)s',
            datefmt='%H:%M:%S'
        )
        # we can change the logging level. Use logging.DEBUG if necesarry
        logger.setLevel(logging.DEBUG)
        self.logger = logger


    def scrape_an_object(self) -> tuple :


    # setting the chrome driver for selenium
        driver = webdriver.Chrome(service=Service(DRIVER_PATH))

    # opening the given URL
        self.logger.debug("Opening the given URL")
        driver.get(self.object_url)
    

    # accepting the cookies
        self.logger.debug("Accepting the cookies")
        driver.find_element(By.CLASS_NAME,"lssxud").click()

    # waiting some random seconds
        time.sleep(random.uniform(4,6))

    # I use CSS selectors where I can, because its more robust than XPATH
        object_name = driver.find_element(
            By.CSS_SELECTOR,
            'h1.DUwDvf.fontHeadlineLarge'
        ).text
        self.logger.debug(f'Object_name OK : {object_name}')

        object_address = driver.find_element(
            By.CSS_SELECTOR,
            'div.Io6YTe.fontBodyMedium'
        ).text
        self.logger.debug(f'Object_address OK : {object_address}')


        try:
            
            overall_rating = driver.find_element(
            By.CSS_SELECTOR,
            'div.F7nice.mmu3tf'
            ).text.split()[0]
            self.logger.debug(f'Overall_rating OK : {overall_rating}')

            review_number = driver.find_element(
            By.CSS_SELECTOR,
            'div.F7nice.mmu3tf'
            ).text.replace(' ','')

            review_number = int(re.compile(r'\d+').findall(review_number)[-1])
            self.logger.debug(f'Review_number OK : {review_number}')

        # click to load further reviews
            driver.find_element(
            By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span'
            ).click()

            self.logger.debug('Clicked to load further reviews')
    
            time.sleep(random.uniform(0.1, 0.5))

        # find scroll layout
            scrollable_div = driver.find_element(
            By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'
            )

            self.logger.debug('Scroll div OK')
     
        except NoSuchElementException:

            self.logger.debug('Except branch')

            div_num_rating = driver.find_element(
            By.CSS_SELECTOR,
            'div.F7nice'
            ).text
            overall_rating = div_num_rating.split()[0]
            self.logger.debug(f'Overall_rating OK : {overall_rating}')

            review_number = int(div_num_rating.split()[1].replace('(','').replace(')',''))
            self.logger.debug(f'Review_number OK : {review_number}')

        # click on the review tab
            driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[1]').click()
            self.logger.debug('clicked to load further reviews')

            time.sleep(random.uniform(0.1, 0.5))

        # find scroll layout
            scrollable_div = driver.find_element(
            By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]'
            )

            self.logger.debug('Scroll div OK')

        time.sleep(random.uniform(2,4))



    # scroll as many times as necessary to load all reviews
        for _ in range(0,(round(review_number/5 - 1)+1)):
            driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollHeight',
            scrollable_div
            )
            time.sleep(random.uniform(1, 2))

    # button lire plus
        button_lire_plus = driver.find_elements(By.CLASS_NAME,'w8nwRe.kyuRq')
        for i in button_lire_plus:
            i.click()


    # parse the html with a bs object
        response = BeautifulSoup(driver.page_source, 'html.parser')
        self.reviews_source = response.find_all('div', class_='jJc9Ad')
        self.logger.debug('Source code has been parsed!')

    # closing the browser
        driver.close()

    # storing the data in a dict
        self.store_main_data = {'object_name': object_name,
                       'object_address': object_address,
                       'overall_rating': overall_rating,
                       'review_num': review_number,
                       'object_url':self.object_url}

        return self.store_main_data, self.reviews_source



    def extract_reviews(self) -> list:

        self.logger.debug('Starting iterate trough the reviews...')
        for review in self.reviews_source:

        # extract the relevant informations
            user = review.find('div', class_= 'd4r55').text.strip()
            date = review.find('span', class_= 'rsqaWe').text.strip()
            rate = len(review.find('span',class_ = 'kvMYJc'))
            review_text = review.find('span', class_= 'wiI7pd')
            review_text = '' if review_text is None else review_text.text 
            reply_source = review.find('div', class_= 'CDe7pd')
            reply = reply_source.text if reply_source else '-'


            self.review_list.append({'name': user,
                            'date': date,
                            'rate': rate,
                            'review_text': review_text,
                            'reply': reply})

        return self.review_list
