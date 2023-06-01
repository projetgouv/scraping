import string
import pandas as pd
from collections import Counter
import re

import streamlit as st

st.set_page_config(page_title='France Echanges', layout='wide', initial_sidebar_state='collapsed')
st.markdown("<h1 style='text-align: center;'>Analyse des tendances nationale</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.write("Afin de mieux comprendre les avis des utilisateurs, nous avons analysé les tendances qui se dégagent des commentaires en utilisant les n-grams. \
        Les n-grams sont des séquences de n mots qui se suivent, où les bi-grams sont des séquences de deux mots, les tri-grams sont des séquences de trois mots, et ainsi de suite.\
        Cette analyse met en évidence les mots et expressions les plus fréquents dans les avis.")

all_data = pd.read_csv('/Users/camille/repo/Hetic/projet_gouv/scraping/Cleaning_eda/all_data.csv')
all_data = all_data.dropna(subset=['cleaned_text'])
all_data = all_data.reset_index(drop=True)
all_data['cleaned_text'] = all_data['cleaned_text'].astype(str)
pos, neg = st.tabs(['Positive', 'Negative'])

with pos:

    pos_texte = all_data[all_data['sentiment'] == 1]['cleaned_text'].str.replace(r'[{}]'.format(re.escape(string.punctuation)), '')
   
    pos_tokens = pos_texte.str.split()

    pos_trigrams = Counter(tuple(trigram) for trigram in pos_tokens if len(trigram) == 3)
    pos_fourgrams = Counter(tuple(bigram) for bigram in pos_tokens if len(bigram) == 2)

    most_common_pos_trigrams = pos_trigrams.most_common(5)
    most_common_pos_fourgrams = pos_fourgrams.most_common(5)
    col1, col2 = st.columns([1, 1])
    with col2:
        st.write("Les trigrams les plus fréquents dans les avis positifs sont:")
        for trigram in most_common_pos_trigrams:
            st.write(f"- {' '.join(trigram[0])}")
    with col1:
        st.write("Les bigrams les plus fréquents dans les avis positifs sont:")
        for bigram in most_common_pos_fourgrams:
            st.write(f"- {' '.join(bigram[0])}")

with neg:
    neg_texte = all_data[all_data['sentiment'] == 0]['cleaned_text'].str.replace(r'[{}]'.format(re.escape(string.punctuation)), '')

    # Split into tokens
    neg_tokens = neg_texte.str.split()

    # Generate trigrams and 2-grams
    neg_trigrams = Counter(tuple(trigram) for trigram in neg_tokens if len(trigram) == 3)
    neg_fourgrams = Counter(tuple(bigram) for bigram in neg_tokens if len(bigram) == 2)

    # Get the most common n-grams
    most_common_neg_trigrams = neg_trigrams.most_common(5)
    most_common_neg_fourgrams = neg_fourgrams.most_common(5)
    col1, col2 = st.columns([1, 1])
    with col2:
        st.write("Les trigrams les plus fréquents dans les avis négatifs sont:")
        for trigram in most_common_neg_trigrams:
            st.write(f"- {' '.join(trigram[0])}")
    with col1:
        st.write("Les bigrams les plus fréquents dans les avis négatifs sont:")
        for bigram in most_common_neg_fourgrams:
            st.write(f"- {' '.join(bigram[0])}")