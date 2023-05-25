import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import re

# Configuration de la page Streamlit
st.set_page_config(page_title='France Echanges', page_icon=':house:', layout='wide')

# Lecture des données à partir du fichier CSV
data = pd.read_csv('all_data/google_reviews_RGPD.csv')

# Fonction pour extraire la ville à partir de l'adresse
def extract_city_from_address(address):
    matches = re.findall(r'\d{5} (.*)', address)
    if matches:
        return matches[0]
    else:
        return None

# Ajout d'une colonne 'city' contenant la ville extraite de l'adresse
data['city'] = data['object_address'].apply(extract_city_from_address)

# Interface Streamlit
st.markdown("<h1 style='text-align: center;'>France Echanges</h1>", unsafe_allow_html=True)

# Nombre total de revues positives et négatives
nb_pos = data['rate'].apply(lambda x: x >= 2.5).sum()
nb_neg = len(data) - nb_pos

# Création du graphique pour toutes les villes
labels = ['Positives', 'Negatives']
values = [nb_pos, nb_neg]
fig_g = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])

col1, col2 = st.columns(2)
with col1:
    st.title('Statistiques globale')
    # Affichage du graphique pour toutes les villes
    st.plotly_chart(fig_g, use_container_width=True)

with col2:
    # Sélection d'une ville spécifique
    selected_city = st.selectbox('Choisissez une ville', data['city'].unique())

    # Filtrage des données pour la ville sélectionnée
    data_city = data[data['city'] == selected_city]

    # Nombre de revues positives et négatives pour la ville sélectionnée
    nb_pos_city = data_city['rate'].apply(lambda x: x >= 2.5).sum()
    nb_neg_city = len(data_city) - nb_pos_city

    # Création du graphique pour la ville sélectionnée
    labels_city = ['Positives', 'Negatives']
    values_city = [nb_pos_city, nb_neg_city]
    fig = go.Figure(data=[go.Pie(labels=labels_city, values=values_city, hole=.5)])

    # Affichage du graphique pour la ville sélectionnée
    st.plotly_chart(fig, use_container_width=True)
