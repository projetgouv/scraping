import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk import ngrams
from collections import Counter
import matplotlib.pyplot as plt

# Charger le modèle de langue français

from data_prep import DataProcessor


# Configuration de la page Streamlit
st.set_page_config(page_title='France Echanges', page_icon=':house:', layout='wide')

st.markdown("<h1 style='text-align: center;'>Analyse de la satisfaction des utilisateurs : panorama national</h1>", unsafe_allow_html=True)
st.markdown("")
# Chargement des données scrappées
data_file = 'all_data/data_all.csv'
df_scraped_data = pd.read_csv(data_file)
columns = ['date', 'rate', 'review_text', 'address', 'latitude', 'longitude']

# Préparation des données
data_processor = DataProcessor(data_file)
data_processor.process_data(columns)
data = data_processor.data

# Calcul des statistiques
nombre_lieux_scrappes = len(df_scraped_data['address'].unique())
addresses_file = 'all_data/pole_emploi.csv'
df_addresses = pd.read_csv(addresses_file)
nombre_lieux = len(df_addresses['Adresse'].unique())
pourcentage_scrappes = round((nombre_lieux_scrappes / nombre_lieux) * 100, 1)
nb_reviews = data.groupby('years').agg({'rate': ['count', 'mean']}).reset_index()
nb_reviews = nb_reviews[nb_reviews['years'] != 'NaT']
nb_reviews.columns = ['years', 'nombre de reviews', 'note moyenne']
nb_reviews['note moyenne'] = round(nb_reviews['note moyenne'], 1)
# Drop année non reconnue

# Note moyenne sur toutes les années
note_moyenne = nb_reviews['note moyenne'].mean()
note_moyenne = round(note_moyenne, 1)
# Année avec la note moyenne la plus élevée
best_year = nb_reviews['years'][nb_reviews['note moyenne'].idxmax()]
# Année avec la note moyenne la plus basse
worst_year = nb_reviews['years'][nb_reviews['note moyenne'].idxmin()]

col1, col2, col3,col4= st.columns(4)
with col1:
    st.metric(label="Nombre de lieux scrappés", value=nombre_lieux_scrappes)
with col2:
    st.metric(label="Nombre d'avis scrappés", value=nb_reviews['nombre de reviews'].sum())

with col3:
    st.metric(label="Pourcentage de lieux scrappés", value=str(pourcentage_scrappes) + "%")
with col4:
    st.metric(label="Note moyenne sur toutes les années", value=note_moyenne)

data['pos'] = data['rate'].apply(lambda x:  x >= 2.5)
#nb de revewies postives 
nb_pos = data['pos'].sum()

#nb de revewies negatives
nb_neg = data['pos'].count() - nb_pos
labels = ['Positives', 'Negatives']
values = [nb_pos, nb_neg]
fig_pos = go.Figure(data=[go.Pie(labels=labels, values=values,  hole=.5, marker=dict(colors=['#0049FF', '#ff0000']))]) 





# Affichage du graphique
line = px.line(nb_reviews, x='years', y='nombre de reviews', text='note moyenne')
line.update_traces(
    hovertemplate='Année: %{x}<br>Nombre de reviews: %{y}<br>Note moyenne: %{text:.1f}')
line.update_traces(textposition='top center')
line.update_layout(xaxis={'type': 'category'})
line.update_layout(title={'text': 'Nombre de reviews et note moyenne par année', 'x': 0.5, 'xanchor': 'center'})


# Affichage du DataFrame
df_grouped = data.groupby('address').agg({'rate': [('average_rate', 'mean'), ('review_count', 'count')], 'latitude': 'first', 'longitude': 'first'}).reset_index()
df_grouped.columns = ['address', 'average_rate', 'review_count', 'latitude', 'longitude']

df_grouped['average_rate'] = df_grouped['average_rate'].round(1)
df_grouped['average_rate'].astype(float)
fig = go.Figure(go.Scattermapbox(
    lat=df_grouped['latitude'],
    lon=df_grouped['longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=10,
        opacity=0.7,

        colorbar=dict(
            title='Note moyenne'
        )
    ),
    text=df_grouped['address'],
    hovertemplate="<b>%{text}</b><br><br>" +
                  "Note moyenne: %{customdata[0]:.1f}<br>" +
                  "Nombre d'avis: %{customdata[1]}<br>" +
                  "<extra></extra>",
    customdata=df_grouped[['average_rate', 'review_count']].values
))

fig.update_layout(
    mapbox_style='carto-positron',
    mapbox_zoom=5,
    mapbox_center={'lat': df_grouped['latitude'].mean(), 'lon': df_grouped['longitude'].mean()},
    height=800
)

fig.update_traces(marker_color=df_grouped['average_rate'])

cola, colb = st.columns(2)
with cola:
    st.plotly_chart(line, use_container_width=True)
with colb:
    st.plotly_chart(fig_pos, use_container_width=True)
st.markdown("<h4 style='text-align: center;'>Lieux scrapés (nombre d'avis et note moyenne)</h4>", unsafe_allow_html=True)



data_sentiment = pd.read_csv('Cleaning_eda/all_data.csv')

neg_reviews = data_sentiment[data_sentiment['sentiment'] == 0]
neg_reviews['cleaned_text'] = neg_reviews['cleaned_text'].astype(str)
neg_reviews.dropna(inplace=True)

pos_reviews = data_sentiment[data_sentiment['sentiment'] == 1]
pos_reviews['cleaned_text'] = pos_reviews['cleaned_text'].astype(str)

neg_reviews_text = ' '.join(neg_reviews['cleaned_text'])
pos_reviews_text = ' '.join(pos_reviews['cleaned_text'])

nlp = spacy.load("fr_core_news_sm")
nlp.max_length = 2000000

dependances_incluses = ['nsubj', 'xcomp', 'obl:mod', 'acl', 'conj', 'amod']
stop_words = spacy.lang.fr.stop_words.STOP_WORDS

# Lemmatisation des termes des avis négatifs
neg_reviews_terms = neg_reviews['cleaned_text'].apply(lambda x: [token.lemma_ for token in nlp(x) if token.dep_ in dependances_incluses and token.text.lower() not in stop_words])
occurrence_terms_neg = Counter([term for terms in neg_reviews_terms for term in terms])

# Lemmatisation des termes des avis positifs
pos_reviews_terms = pos_reviews['cleaned_text'].apply(lambda x: [token.lemma_ for token in nlp(x) if token.dep_ in dependances_incluses and token.text.lower() not in stop_words])
occurrence_terms_pos = Counter([term for terms in pos_reviews_terms for term in terms])


wordcloud_neg = WordCloud(background_color="white", colormap= 'Reds').generate_from_frequencies(occurrence_terms_neg)
wordcloud_pos = WordCloud(background_color="white", colormap= 'Blues_r').generate_from_frequencies(occurrence_terms_pos)

fig_neg = plt.figure(figsize=(10, 6))
plt.imshow(wordcloud_neg, interpolation='bilinear')
plt.axis('off')
plt.title('Nuage de mots des termes les plus fréquents dans les avis négatifs')
plt.show()

fig_pos = plt.figure(figsize=(10, 6))
plt.imshow(wordcloud_pos, interpolation='bilinear')
plt.axis('off')
plt.title('Nuage de mots des termes les plus fréquents dans les avis positifs')
plt.show()


with cola:
    st.pyplot(fig_neg)
with colb:
    st.pyplot(fig_pos)

st.plotly_chart(fig, use_container_width=True)