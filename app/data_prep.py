import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

class DataProcessor:
    def __init__(self, path):
        self.path = path
        self.data = None
    
    def load_data(self, columns):
        self.data = pd.read_csv(self.path, usecols=columns)
    
    def clean_date_column(self):
        replacements = {
            'a day ago': '1 day ago',
            'a year ago': '1 year ago',
            'a month ago': '1 month ago',
            'a week ago': '1 week ago'
        }
        self.data['date'] = self.data['date'].replace(replacements)
        
        current_datetime = datetime.now()
        self.data['date'] = self.data['date'].apply(lambda x: current_datetime - relativedelta(years=int(x.split()[0])) if 'year' in x
                                                    else current_datetime - relativedelta(months=int(x.split()[0])) if 'month' in x
                                                    else current_datetime - relativedelta(weeks=int(x.split()[0])) if 'week' in x
                                                    else current_datetime - relativedelta(days=int(x.split()[0])) if 'day' in x
                                                    else None)
        
        self.data['date'] = self.data['date'].apply(lambda x: x.date() if x else None)
    
    def group_by_year(self):
        self.data['years'] = pd.to_datetime(self.data['date']).dt.to_period('Y').astype(str)
    
    def process_data(self, columns):
        self.load_data(columns)
        self.clean_date_column()
        self.group_by_year()

class Classement:
    def __init__(self, data_path, location_path):
        self.data_path = data_path
        self.location_path = location_path
        self.data = None
        self.loc = None
        self.load_data()
        self.load_location_data()
    
    def load_data(self):
        
        self.data = pd.read_csv(self.data_path)
    
    def clean_date_column(self):
        replacements = {
            'a year ago': '1 year ago',
            'a month ago': '1 month ago',
            'a week ago': '1 week ago'
        }
        self.data['date'] = self.data['date'].replace(replacements)
        
        current_datetime = datetime.now()
        self.data['date'] = self.data['date'].apply(lambda x: current_datetime - relativedelta(years=int(x.split()[0])) if 'year' in x
                                                    else current_datetime - relativedelta(months=int(x.split()[0])) if 'month' in x
                                                    else current_datetime - relativedelta(weeks=int(x.split()[0])) if 'week' in x
                                                    else current_datetime - relativedelta(days=int(x.split()[0])) if 'day' in x
                                                    else None)
        
        self.data['date'] = self.data['date'].apply(lambda x: x.date() if x else None)
    
    def load_location_data(self):
        self.loc = pd.read_csv(self.location_path, sep=';')
        self.loc.rename(columns={'adresse': 'address'}, inplace=True)
        self.loc['address'] = self.loc['address'].str.lower().str.strip()
        self.data['address'] = self.data['address'].str.lower().str.strip()

        # Remove comma
        self.data['address'] = self.data['address'].str.replace(',', '')

 
        self.data.drop(self.data[self.data['address'] == 'ƒadam'].index, inplace=True)
    
    def calculate_ranking(self):
        df_lieu = self.data.groupby(['address']).agg(count_rate=('rate', 'count'), mean_rate=('rate', 'mean')).reset_index()
        return df_lieu

    def max_rate(self):
        max_rate = self.data.groupby('address')['rate'].mean().nlargest(1)
        return max_rate

    def min_rate(self):
        min_rate = self.data.groupby('address')['rate'].mean().nsmallest(1)
        return min_rate