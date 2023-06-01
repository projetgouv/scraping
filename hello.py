import pandas as pd

data_exp = pd.read_csv('/Users/camille/repo/Hetic/projet_gouv/scraping/export-experiences.csv', sep='\t', encoding='latin-1')



new_df = pd.DataFrame()

# Colonne 'Information/Explication_neg'
new_df['pos_info'] = data_exp['Information/Explication'].apply(lambda x: 1 if x == 'Positif' else 0)
new_df['neg_info'] = data_exp['Information/Explication'].apply(lambda x: 1 if x == 'Négatif' else 0)

new_df['pos_access'] = data_exp['Accessibilité'].apply(lambda x: 1 if x == 'Positif' else 0)
new_df['neg_access'] = data_exp['Accessibilité'].apply(lambda x: 1 if x == 'Négatif' else 0)

new_df['pos_relation'] = data_exp['Relation'].apply(lambda x: 1 if x == 'Positif' else 0)
new_df['neg_relation'] = data_exp['Relation'].apply(lambda x: 1 if x == 'Négatif' else 0)

new_df['pos_reactivite'] = data_exp['Réactivité'].apply(lambda x: 1 if x == 'Positif' else 0)
new_df['neg_reactivite'] = data_exp['Réactivité'].apply(lambda x: 1 if x == 'Négatif' else 0)

new_df['pos_simplicite'] = data_exp['Simplicité/Complexité'].apply(lambda x: 1 if x == 'Positif' else 0)
new_df['neg_simplicite'] = data_exp['Simplicité/Complexité'].apply(lambda x: 1 if x == 'Négatif' else 0)

# Colonne 'text'
new_df['Description'] = data_exp['Description']
from sklearn.model_selection import train_test_split

train, test = train_test_split(new_df, random_state=42, test_size=0.30, shuffle=True)
train_text = train['Description']
test_text = test['Description']
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2')
vectorizer.fit(train_text)
vectorizer.fit(test_text)
categories = list(new_df.columns.values)
categories = categories[:-1]
print(categories)
x_train = vectorizer.transform(train_text)
y_train = train.drop(labels = ['Description'], axis=1)

x_test = vectorizer.transform(test_text)
y_test = test.drop(labels = ['Description'], axis=1)
from skmultilearn.problem_transform import BinaryRelevance
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# initialize binary relevance multi-label classifier with RandomForestClassifier
classifier = BinaryRelevance(RandomForestClassifier())

# train
classifier.fit(x_train, y_train)

# predict
predictions = classifier.predict(x_test)

# accuracy
accuracy = accuracy_score(y_test, predictions)
print("Accuracy =", accuracy)
