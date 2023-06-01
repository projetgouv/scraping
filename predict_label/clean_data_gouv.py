import pandas as pd
from nltk.corpus import stopwords
import spacy
data_exp = pd.read_csv('/Users/camille/repo/Hetic/projet_gouv/scraping/export-experiences.csv', sep='\t', encoding='latin-1')



new_df = pd.DataFrame()

# Colonne 'Information/Explication_neg'
new_df['pos_info'] = data_exp['Information/Explication'].apply(lambda x: 1 if x == 'Positif' else 0)
new_df['neg_info'] = data_exp['Information/Explication'].apply(lambda x: 1 if x == 'Négatif' else 0)
new_df['neutre_info'] = data_exp['Information/Explication'].apply(lambda x: 1 if x == 'Neutre' else 0)
new_df['unknown_info'] = data_exp['Information/Explication'].apply(lambda x: 1 if pd.isna(x) else 0)



new_df['pos_access'] = data_exp['Accessibilité'].apply(lambda x: 1 if x == 'Positif' else 0)
new_df['neg_access'] = data_exp['Accessibilité'].apply(lambda x: 1 if x == 'Négatif' else 0)
new_df['neutre_access'] = data_exp['Accessibilité'].apply(lambda x: 1 if x == 'Neutre' else 0)
new_df['unknown_access'] = data_exp['Accessibilité'].apply(lambda x: 1 if pd.isna(x) else 0)

new_df['pos_relation'] = data_exp['Relation'].apply(lambda x: 1 if x == 'Positif' else 0)
new_df['neg_relation'] = data_exp['Relation'].apply(lambda x: 1 if x == 'Négatif' else 0)
new_df['neutre_relation'] = data_exp['Relation'].apply(lambda x: 1 if x == 'Neutre' else 0)
new_df['unknown_relation'] = data_exp['Relation'].apply(lambda x: 1 if pd.isna(x) else 0)

new_df['pos_reactivite'] = data_exp['Réactivité'].apply(lambda x: 1 if x == 'Positif' else 0)
new_df['neg_reactivite'] = data_exp['Réactivité'].apply(lambda x: 1 if x == 'Négatif' else 0)
new_df['neutre_reactivite'] = data_exp['Réactivité'].apply(lambda x: 1 if x == 'Neutre' else 0)
new_df['unknown_reactivite'] = data_exp['Réactivité'].apply(lambda x: 1 if pd.isna(x) else 0)

new_df['pos_simplicite'] = data_exp['Simplicité/Complexité'].apply(lambda x: 1 if x == 'Positif' else 0)
new_df['neg_simplicite'] = data_exp['Simplicité/Complexité'].apply(lambda x: 1 if x == 'Négatif' else 0)
new_df['neutre_simplicite'] = data_exp['Simplicité/Complexité'].apply(lambda x: 1 if x == 'Neutre' else 0)
new_df['unknown_simplicite'] = data_exp['Simplicité/Complexité'].apply(lambda x: 1 if pd.isna(x) else 0)
# Colonne 'text'
new_df['Description'] = data_exp['Description']
new_df['Description'] = new_df['Description'].str.lower()
# delete punctuation
new_df['Description'] = new_df['Description'].str.replace('[^\w\s]','')
print("Ponctuation supprimée")
# french stop words

stop = stopwords.words('french')
new_df['Description'] = new_df['Description'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
#lemmatisation avex spacy

nlp = spacy.load('fr_core_news_sm')
new_df['Description'] = new_df['Description'].apply(lambda x: " ".join([token.lemma_ for token in nlp(x)]))
print("Lemmatisation effectuée")
# Save df to csv
new_df.to_csv('/Users/camille/repo/Hetic/projet_gouv/scraping/predict_label/data_exp_clean.csv', sep='\t', encoding='latin-1')