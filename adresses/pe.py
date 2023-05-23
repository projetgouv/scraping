import pandas as pd
import os

# Charger le fichier CSV contenant les données de scraping
data_file = '/Users/camille/repo/Hetic/projet_gouv/scraping/output/google_reviews.csv'
df_scraped_data = pd.read_csv(data_file)

# Chemin du fichier contenant les adresses
addresses_file = '/Users/camille/repo/Hetic/projet_gouv/scraping/pole_emploi.csv'

# Charger les adresses depuis le fichier
df_addresses = pd.read_csv(addresses_file)

# Obtenir tous les noms des lieux
all_places = df_addresses['Adresse'].tolist()

# Obtenir les noms des lieux présents dans le DataFrame de scraping
scraped_places = df_scraped_data['object_name'].tolist()

# Trouver les lieux qui n'ont pas été scrapés
missing_places = list(set(all_places) - set(scraped_places))
num_missing_places = len(missing_places)

# Enregistrer les noms des lieux non scrapés et le nombre d'objets non scrapés dans un fichier texte
output_file = '/Users/camille/repo/Hetic/projet_gouv/scraping/output/missing_places.txt'
with open(output_file, 'w') as f:
    f.write("Lieux manquants :\n")
    for place in missing_places:
        f.write(place + '\n')
    f.write(f"\nNombre d'objets non scrapés : {num_missing_places}")

print("Les lieux manquants ont été enregistrés dans le fichier 'missing_places.txt'.")
