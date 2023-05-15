from constants import *
from utils import *
from logsetting import setfunction
from url_generator import UrlGenerator
from scraping import MyScraper

logger = setfunction(lenom='main')

df = pd.read_csv(ORIGIN_PATH, sep=';')

url_objet = UrlGenerator(dataframe = df)
list_urls = url_objet.generate_urls()


scraped_data =  []

    # loop trough the urls and calling the necessary functions to populate the empty scraped_data list
for i, url in enumerate(list_urls):
    try:
        time.sleep(random.uniform(3,10))

        scrap_objet = MyScraper(object_url = url)
        store_main_data, reviews_source = scrap_objet.scrape_an_object()
        scraped_data.append(store_main_data)

        review_list = scrap_objet.extract_reviews()
        scraped_data[i]['reviews'] = review_list
        print (scraped_data[i]['review_num'], len(scraped_data[i]['reviews']))

        if scraped_data[i]['review_num'] != len(scraped_data[i]['reviews']):
            logger.warning(f'For some reason not all the reviews had been scraped for the following object: {store_main_data["object_name"]}')


    except Exception as exception:
        logger.error(f'{url} \n {exception}')
        scraped_data.append(
                {'object_name': 'Error',
                'object_address': 'Error',
                'overall_rating': 'None',
                'review_num': 'None',
                'object_url':url,
                'reviews':[{}]
                }
            )

    logger.info(f' {i+1} URL has been finished from the total of {len(list_urls)}')


# reading the dict with pandas
#print(scraped_data)
result_df = pd.json_normalize(
            scraped_data,
            record_path = ['reviews'],
            errors='ignore',
            meta=['object_name', 'object_address', 'overall_rating', 'review_num', 'object_url']
            )


# reorder the columns


# Saving the result into an excel file
save_path = os.path.join(SAVING_PATH,'scrape_result.csv')
result_df.to_csv(
    save_path,
    index= False
)

logger.info(f'Successfully exported the result file in the following folder: {os.path.join(SAVING_PATH,"scrape_result.csv")}')
logger.info('Finished!')