# Ouvrir le fichier texte en mode lecture
with open("projet_lois_clean_without_top_words.txt", "r") as f:
    # Lire le contenu du fichier dans une chaîne de caractères
    projet_lois_clean_without_top_words_str = f.read()

# Afficher la longueur de la chaîne de caractères pour vérifier que tout fonctionne correctement
# Diviser la chaîne de caractères en une liste de documents
projet_lois_clean_docs = projet_lois_clean_without_top_words_str.split("\n")

# Retirer les documents vides éventuels de la liste
projet_lois_clean_docs = [doc.strip() for doc in projet_lois_clean_docs if len(doc.strip()) > 0]

# Afficher le nombre de documents dans la liste
print(len(projet_lois_clean_docs))

# Appliquer BERTopic sur les documents
from bertopic import BERTopic

topic_model = BERTopic(language="multilingual")
topics, probs = topic_model.fit_transform(projet_lois_clean_docs)
