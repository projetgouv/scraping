import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

from data_prep import DataProcessor

# Configuration de la page Streamlit
st.set_page_config(page_title='France Echange', page_icon=':house:', layout='wide')

# Interface Streamlit
st.markdown("<h1 style='text-align: center;'>Avis par structre </h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Choisissez un lieu afin de connaitre ses statistiques</h4>", unsafe_allow_html=True)

data_path = 'all_data/google_reviews_RGPD.csv'
columns = ['date', 'rate', 'review_text', 'object_address']

processor = DataProcessor(data_path)
processor.process_data(columns)
data = processor.data

#Load data2
data_path = 'predict_label/result_df.csv'

# Vous pouvez accéder aux données transformées via l'attribut `data` de l'objet `processor`
location_path = 'Data/location.csv'
# Vous pouvez accéder aux données transformées via l'attribut `data` de l'objet `proc ssor`
worst_best = data.groupby('object_address').agg({'rate': ['count', 'mean']}).reset_index()
worst_best = worst_best[worst_best[('rate', 'count')] >= 10]  # Filter locations with count >= 10
worst_place = worst_best.sort_values(('rate', 'mean'), ascending=True).head(1)
best_place = worst_best.sort_values(('rate', 'mean'), ascending=False).head(1)

worst_place_name = (worst_place.iloc[0]['object_address']).values[0]
worst_place_rating = float(worst_place.iloc[0][('rate', 'mean')])
worst_place_count = str(worst_place.iloc[0][('rate', 'count')])

best_place_name = (best_place.iloc[0]['object_address']).values[0]
best_place_rating = best_place.iloc[0][('rate', 'mean')]
best_place_count = best_place.iloc[0][('rate', 'count')]

worst_place_text = f"{worst_place_name} ({worst_place_count} avis)"
best_place_text = f"{best_place_name} ({best_place_count} avis)"

selected_lieux = st.selectbox('Choisissez un lieu', data['object_address'].unique())

# Filter data based on selected location
selected_data = data[data['object_address'] == selected_lieux]

nb_reviews = selected_data.groupby('years').agg({'rate': ['count', 'mean']}).reset_index()
nb_reviews.columns = ['years', 'nombre de reviews', 'note moyenne']
nb_reviews['note moyenne'] = nb_reviews['note moyenne'].round(1)

# Créer un graphique avec l'année, le nombre de reviews et la note moyenne
fig = go.Figure()

# Ajouter la ligne pour la note moyenne
fig.add_trace(go.Scatter(
    x=nb_reviews['years'],
    y=nb_reviews['note moyenne'],
    text=nb_reviews['note moyenne'],
    mode='lines',
    name='Note moyenne',
    line=dict(color='#ff0000'),
    hovertemplate='Note moyenne: %{text:.1f}'
))

# Ajouter les barres pour le nombre d'avis
fig.add_trace(go.Bar(
    x=nb_reviews['years'],
    y=nb_reviews['nombre de reviews'],
    text=nb_reviews['nombre de reviews'],
    name='Nombre d\'avis',
    textposition='auto',
    marker=dict(
        color='#0049FF'  # Couleur bleu foncé
    )
))

# Mise en forme de la figure
fig.update_layout(
    xaxis={'type': 'category'},
    title={'text': 'Nombre de reviews et note moyenne par année', 'x': 0.5, 'xanchor': 'center'}
)


# Filter out reviews for the current year
current_year = pd.Timestamp.now().year
filtered_reviews = nb_reviews[nb_reviews['years'] != str(current_year)]

# Find the worst place and its rating from the entire dataset
worst_place = data['object_address'][data['rate'].idxmin()]
worst_rating = data['rate'].min().round(1)

# Display the worst place and its rating


# Display the metric values for other statistics
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(label="Nombre de reviews", value=nb_reviews['nombre de reviews'].sum())

with col2:
    st.metric(label="Note moyenne", value=nb_reviews['note moyenne'].mean().round(1))

with col3:
    st.metric(label="Nombre moyen de reviews par an", value=nb_reviews['nombre de reviews'].mean().round(1))
with col4:
    st.metric(label="Année avec la meilleure note moyenne", value=filtered_reviews['years'][filtered_reviews['note moyenne'].idxmax()])
with col5:
    st.metric(label="Année avec la pire note moyenne", value=filtered_reviews['years'][filtered_reviews['note moyenne'].idxmin()])

col1, col2 = st.columns(2)
with col1:
    st.write(f"Le lieu avec la note la plus basse est {worst_place_text} avec une note de {worst_place_rating}")
with col2:
    st.write(f"Le lieu avec la meilleure note est {best_place_text} avec une note de {best_place_rating}")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    data_city = data[data['object_address'] == selected_lieux]

    # Nombre de revues positives et négatives pour la ville sélectionnée
    nb_pos_city = data_city['rate'].apply(lambda x: x >= 2.5).sum()
    nb_neg_city = len(data_city) - nb_pos_city

    # Création du graphique pour la ville sélectionnée
    labels_city = ['Positives', 'Negatives']
    values_city = [nb_pos_city, nb_neg_city]
    fig_city = go.Figure(data=[go.Pie(labels=labels_city, values=values_city, hole=.5, marker=dict(colors=['#0049FF', '#ff0000']))])

    # Affichage du graphique pour la ville sélectionnée
    st.plotly_chart(fig_city, use_container_width=True)
df_pos_reviews = pd.read_csv('Cleaning_eda/all_data_pos.csv')
# on doit prendre en comptes la lieux selectionnés
df_pos_reviews = df_pos_reviews[df_pos_reviews['object_address'] == selected_lieux]
pos_reviews_terms = []
df_pos_reviews['pos_reviews_terms'].apply(lambda x: pos_reviews_terms.extend(eval(x)))
df_neg_reviews = pd.read_csv('Cleaning_eda/all_data_neg.csv')
# on doit prendre en comptes la lieux selectionnés
df_neg_reviews = df_neg_reviews[df_neg_reviews['object_address'] == selected_lieux]
neg_reviews_terms = []
df_neg_reviews['neg_reviews_terms'].apply(lambda x: neg_reviews_terms.extend(eval(x))).astype(str)
occurrence_terms_neg = Counter(neg_reviews_terms)
occurrence_terms_pos = Counter(pos_reviews_terms)


wordcloud_neg = WordCloud(background_color="white", colormap= 'Reds').generate_from_frequencies(occurrence_terms_neg)
wordcloud_pos = WordCloud(background_color="white", colormap= 'Blues_r').generate_from_frequencies(occurrence_terms_pos)

fig_neg = plt.figure(figsize=(10, 6))
plt.imshow(wordcloud_neg, interpolation='bilinear')
plt.axis('off')

plt.show()

fig_pos = plt.figure(figsize=(10, 6))
plt.imshow(wordcloud_pos, interpolation='bilinear')
plt.axis('off')
plt.show()

with col1:
    st.markdown("<h4 style='text-align: center;'>Nuage de mots des termes les plus fréquents dans les avis négatifs</h4>", unsafe_allow_html=True)
    st.pyplot(fig_neg)
with col2:
    st.markdown("<h4 style='text-align: center;'>Nuage de mots des termes les plus fréquents dans les avis positifs</h4>", unsafe_allow_html=True)
    st.pyplot(fig_pos)



df = pd.read_csv('predict_label/result_pos_df.csv')
# on doit prendre en comptes la lieux selectionnés prcédemment
df = df[df['object_address'] == selected_lieux]
percentage_neg_info_predicted = round(df['neg_info_predicted'].sum() / len(df['neg_info_predicted']) * 100)
percentage_pos_info_predicted = round(df['pos_info_predicted'].sum() / len(df['pos_info_predicted']) * 100)
percentage_neutre_info_predicted = round(df['neutre_info_predicted'].sum() / len(df['neutre_info_predicted']) * 100)
percentage_pos_access_predicted = round(df['pos_access_predicted'].sum() / len(df['pos_access_predicted']) * 100)
percentage_neg_access_predicted = round(df['neg_access_predicted'].sum() / len(df['neg_access_predicted']) * 100)
percentage_neutre_access_predicted = round(df['neutre_access_predicted'].sum() / len(df['neutre_access_predicted']) * 100)

percentage_pos_relation_predicted = round(df['pos_relation_predicted'].sum() / len(df['pos_relation_predicted']) * 100)
percentage_neg_relation_predicted = round(df['neg_relation_predicted'].sum() / len(df['neg_relation_predicted']) * 100)
percentage_neutre_relation_predicted = round(df['neutre_relation_predicted'].sum() / len(df['neutre_relation_predicted']) * 100)

percentage_pos_reactivite_predicted = round(df['pos_reactivite_predicted'].sum() / len(df['pos_reactivite_predicted']) * 100)
percentage_neg_reactivite_predicted = round(df['neg_reactivite_predicted'].sum() / len(df['neg_reactivite_predicted']) * 100)
percentage_neutre_reactivite_predicted = round(df['neutre_reactivite_predicted'].sum() / len(df['neutre_reactivite_predicted']) * 100)

percentage_pos_simplicite_predicted = round(df['pos_simplicite_predicted'].sum() / len(df['pos_simplicite_predicted']) * 100)
percentage_neg_simplicite_predicted = round(df['neg_simplicite_predicted'].sum() / len(df['neg_simplicite_predicted']) * 100)
percentage_neutre_simplicite_predicted = round(df['neutre_simplicite_predicted'].sum() / len(df['neutre_simplicite_predicted']) * 100)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(label="Ressenti négatif sur l'info", value=f"{percentage_neg_info_predicted}%")
    st.metric(label="Ressenti positif sur l'info", value=f"{percentage_pos_info_predicted}%")
    st.metric(label="Ressenti neutre sur l'info", value=f"{percentage_neutre_info_predicted}%")

with col2:
    st.metric(label="Ressenti positif sur l'accès", value=f"{percentage_pos_access_predicted}%")
    st.metric(label="Ressenti négatif sur l'accès", value=f"{percentage_neg_access_predicted}%")
    st.metric(label="Ressenti neutre sur l'accès", value=f"{percentage_neutre_access_predicted}%")

with col3:
    st.metric(label="Ressenti positif sur la relation", value=f"{percentage_pos_relation_predicted}%")
    st.metric(label="Ressenti négatif sur la relation", value=f"{percentage_neg_relation_predicted}%")
    st.metric(label="Ressenti neutre sur la relation", value=f"{percentage_neutre_relation_predicted}%")

with col4:
    st.metric(label="Ressenti positif sur la réactivité", value=f"{percentage_pos_reactivite_predicted}%")
    st.metric(label="Ressenti négatif sur la réactivité", value=f"{percentage_neg_reactivite_predicted}%")
    st.metric(label="Ressenti neutre sur la réactivité", value=f"{percentage_neutre_reactivite_predicted}%")

with col5:
    st.metric(label="Ressenti positif sur la simplicité", value=f"{percentage_pos_simplicite_predicted}%")
    st.metric(label="Ressenti négatif sur la simplicité", value=f"{percentage_neg_simplicite_predicted}%")
    st.metric(label="Ressenti neutre sur la simplicité", value=f"{percentage_neutre_simplicite_predicted}%")

