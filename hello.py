import pandas as pd

# Charger le fichier CSV contenant les données
data_file = '/Users/camille/repo/Hetic/projet_gouv/scraping/app/data_with_coordinates.csv'
df_data = pd.read_csv(data_file)

# Effectuer la moyenne sur la colonne "rate" en regroupant par "address" et conserver les colonnes "latitude" et "longitude"
df_grouped = df_data.groupby('object_address').agg({'rate': 'mean', 'latitude': 'first', 'longitude': 'first'}).reset_index()

# Afficher le résultat
print(df_grouped)
