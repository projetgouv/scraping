import pandas as pd
import spacy

# Charger le modèle de langue français
nlp = spacy.load("fr_core_news_sm")
nlp.max_length = 2000000

data_sentiment = pd.read_csv('Cleaning_eda/all_data.csv')
nlp.max_length = 2000000

dependances_incluses = ['nsubj', 'xcomp', 'obl:mod', 'acl', 'conj', 'amod']
stop_words = spacy.lang.fr.stop_words.STOP_WORDS
neg_reviews = data_sentiment[data_sentiment['sentiment'] == 0]
neg_reviews['cleaned_text'] = neg_reviews['cleaned_text'].astype(str)
neg_reviews.dropna(inplace=True)

pos_reviews = data_sentiment[data_sentiment['sentiment'] == 1]
pos_reviews['cleaned_text'] = pos_reviews['cleaned_text'].astype(str)

# Lemmatisation des termes des avis négatifs
neg_reviews_terms = neg_reviews['cleaned_text'].apply(lambda x: [token.lemma_ for token in nlp(x) if token.dep_ in dependances_incluses and token.text.lower() not in stop_words])

# Lemmatisation des termes des avis positifs
pos_reviews_terms = pos_reviews['cleaned_text'].apply(lambda x: [token.lemma_ for token in nlp(x) if token.dep_ in dependances_incluses and token.text.lower() not in stop_words])

# Ajouter les colonnes pos_reviews_terms et neg_reviews_terms au DataFrame
neg_reviews['neg_reviews_terms'] = neg_reviews_terms
pos_reviews['pos_reviews_terms'] = pos_reviews_terms

# Enregistrement des données avec les colonnes ajoutées
neg_reviews.to_csv('Cleaning_eda/all_data_neg.csv', index=False)
pos_reviews.to_csv('Cleaning_eda/all_data_pos.csv', index=False)
