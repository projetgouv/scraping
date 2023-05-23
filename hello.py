from app.data_prep import Classement
location_path = '/Users/camille/repo/Hetic/projet_gouv/scraping/Data/location.csv'
data_path = '/Users/camille/repo/Hetic/projet_gouv/scraping/Data/google_reviews.csv'
classment = Classement(data_path, location_path)
classment.load_data()
average_ratings_data = classment.average_ratings()