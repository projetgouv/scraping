import streamlit as st
import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
st.set_page_config(page_title='France Echange', layout='wide', initial_sidebar_state='collapsed')
st.markdown("<h1 style='text-align: center;'>France Echange construisons ensemble le service publique de l'emploi</h1>", unsafe_allow_html=True)
data = pd.read_csv('Cleaning_eda/all_data.csv')
data.dropna(subset=['review_text'], inplace=True)
data.reset_index(drop=True, inplace=True)
pos_data = data[data['sentiment'] ==1]
neg_data = data[data['sentiment'] ==0]
BERTopic(language="multilingual") 
sentence_model = SentenceTransformer("paraphrase-albert-small-v2")
topic_model_pos = BERTopic(embedding_model=sentence_model, nr_topics=5)
pos_data['cleaned_text'] = pos_data['cleaned_text'].astype(str)
pos_data.reset_index(drop=True, inplace=True)
topics, probs = topic_model_pos.fit_transform(pos_data['cleaned_text'])
topics_to_merge = [-1, 1]
topic_model_pos.merge_topics(pos_data['cleaned_text'], topics_to_merge)
fig_pos = topic_model_pos.visualize_barchart()
st.plotly_chart(fig_pos)

# faire de même pour les négatifs, c'est le même code
topic_model_neg = BERTopic(embedding_model=sentence_model, nr_topics=5)
neg_data['cleaned_text'] = neg_data['cleaned_text'].astype(str)
neg_data.reset_index(drop=True, inplace=True)
topics, probs = topic_model_neg.fit_transform(neg_data['cleaned_text'])
topics_to_merge = [-1, 1]
topic_model_neg.merge_topics(neg_data['cleaned_text'], topics_to_merge)
fig_neg = topic_model_neg.visualize_barchart()
st.plotly_chart(fig_neg)                                    
