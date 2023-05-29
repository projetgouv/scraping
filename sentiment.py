import pandas as pd
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification

all_data = pd.read_csv('/Users/camille/repo/Hetic/projet_gouv/scraping/Cleaning_eda/all_data.csv')
all_data = all_data.sample(100)  # Prendre un échantillon de 100 lignes

def preprocess_text(text):
    if isinstance(text, str):
        text = re.sub(r"[^a-zA-ZÀ-ú]", " ", text)
        text = text.lower()
        processed_text = " ".join(text.split())
        return processed_text
    else:
        return ""

preprocessed_corpus = [preprocess_text(cleaned_text) for cleaned_text in all_data['cleaned_text']]

negative_reviews = []
positive_reviews = []
tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine", use_fast=True)
model = TFAutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine")

for i, review in tqdm(enumerate(preprocessed_corpus), desc='Analyzing reviews'):
    inputs = tokenizer.encode_plus(review, add_special_tokens=True, return_tensors="tf", padding=True, truncation=True)
    input_ids = inputs["input_ids"].numpy()[0]
    outputs = model(inputs)
    predicted_label = outputs.logits.numpy().argmax()
    
    if all_data.loc[all_data.index[i], 'sentiment'] == 1:
        if predicted_label == 0:
            negative_reviews.append((i, review))
        else:
            positive_reviews.append((i, review))
    else:
        if predicted_label == 0:
            positive_reviews.append((i, review))
        else:
            negative_reviews.append((i, review))

stopwords = set(stopwords.words("french"))
vectorizer = TfidfVectorizer(stop_words=list(stopwords))
ctfidf_matrix_negative = vectorizer.fit_transform([review for _, review in tqdm(negative_reviews, desc='Creating c-TF-IDF matrix for negative reviews')])

ctfidf_matrix_positive = vectorizer.transform([review for _, review in tqdm(positive_reviews, desc='Creating c-TF-IDF matrix for positive reviews')])

feature_names = vectorizer.get_feature_names_out()
top_negative_words = []

for i in tqdm(range(ctfidf_matrix_negative.shape[0]), desc='Extracting top negative words'):
    review_ctfidf_scores = ctfidf_matrix_negative[i].toarray()[0]
    top_indices = review_ctfidf_scores.argsort()[-10:][::-1]
    review_negative_words = [feature_names[idx] for idx in top_indices if feature_names[idx] not in stopwords]
    top_negative_words.extend(review_negative_words)

top_negative_words = list(set(top_negative_words))

top_positive_words = []

for i in tqdm(range(ctfidf_matrix_positive.shape[0]), desc='Extracting top positive words'):
    review_ctfidf_scores = ctfidf_matrix_positive[i].toarray()[0]
    top_indices = review_ctfidf_scores.argsort()[-10:][::-1]
    review_positive_words = [feature_names[idx] for idx in top_indices if feature_names[idx] not in stopwords]
    top_positive_words.extend(review_positive_words)

top_positive_words = list(set(top_positive_words))

all_data['top_negative_words'] = ""
all_data['top_positive_words'] = ""

for idx, review in tqdm(negative_reviews, desc='Updating negative words'):
    all_data.at[all_data.index[idx], 'top_negative_words'] = ", ".join(top_negative_words)

for idx, review in tqdm(positive_reviews, desc='Updating positive words'):
    all_data.at[all_data.index[idx], 'top_positive_words'] = ", ".join(top_positive_words)

all_data.to_csv('updated_data.csv', index=False)

print("Analysis completed and updated data saved to 'updated_data.csv'.")
