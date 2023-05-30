
import spacy
import pandas as pd
from collections import Counter
from itertools import tee, islice

nlp = spacy.load('fr_core_news_sm')
nlp.max_length = 3000000

all_data = pd.read_csv('/Users/camille/repo/Hetic/projet_gouv/scraping/Cleaning_eda/all_data.csv')

texte= " ".join(all_data['review_text'])
doc = nlp(texte)

# Fonction pour conserver les phrases
def keep_sentences(doc):
    for sent in doc.sents:
        yield sent

# Lemmatisation des tokens
lemmatized_tokens = [token.lemma_ for sentence in keep_sentences(doc) for token in sentence]

# Génération des bi-grammes et tri-grammes
bi_grams = Counter(zip(lemmatized_tokens, islice(lemmatized_tokens, 1, None)))
tri_grams = Counter(zip(lemmatized_tokens, islice(lemmatized_tokens, 1, None), islice(lemmatized_tokens, 3, None)))

# Affichage des bi-grammes les plus courants
print("Bi-grammes les plus courants:")
for bi_gram, count in bi_grams.most_common(10):
    print(bi_gram, ":", count)

# Affichage des tri-grammes les plus courants
print("\nTri-grammes les plus courants:")
for tri_gram, count in tri_grams.most_common(10):
    print(tri_gram, ":", count)