import requests
import csv

url = "https://etablissements-publics.api.gouv.fr/v3/organismes/pole_emploi"
params = {}

response = requests.get(url, params=params)
data = response.json()

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Ouvrir un fichier CSV en mode écriture
    with open("pole_emploi.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Écrire l'en-tête du CSV
        writer.writerow(["Nom", "Adresse"])

        # Parcourir les données et extraire le nom et l'adresse
        for feature in data["features"]:
            for elem in feature:
                properties = elem["properties"]
                nom = properties["nom"]
                adresse = properties["adresses"][0]["lignes"][0]
                writer.writerow([nom, adresse])

    print("Le fichier CSV a été créé avec succès.")
else:
    print("La requête a échoué avec le code d'erreur :", response.status_code)
