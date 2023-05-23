import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_prep import DataProcessor

# Configuration de la page Streamlit
st.set_page_config(page_title='France Echanges', page_icon=':house:', layout='wide')

# Titre et description
st.markdown("<h1 style='text-align: center;'>France Echanges</h1>", unsafe_allow_html=True)
st.write("Bienvenue sur France Echanges, Ensemble, construisons le service public de l'emploi du futur en donnant la parole aux usagers")
st.write("Nous avons rencontré quelques problèmes techniques, avec des données qui ne se sont pas chargées, vous trouvez ci-dessous une analyse des données qui ont pu être chargées")

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

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Nombre de lieux scrappés", value=nombre_lieux_scrappes)
    st.metric(label="Note moyenne sur toutes les années", value=note_moyenne)
with col2:
    st.metric(label="Nombre d'avis scrappés", value=nb_reviews['nombre de reviews'].sum())
    st.metric(label="Année avec la meilleure note moyenne", value=best_year)
with col3:
    st.metric(label="Pourcentage de lieux scrappés", value=str(pourcentage_scrappes) + "%")
    st.metric(label="Année avec la pire note moyenne", value=worst_year)

# Affichage du graphique
fig = px.line(nb_reviews, x='years', y='nombre de reviews', text='note moyenne')
fig.update_traces(
    hovertemplate='Année: %{x}<br>Nombre de reviews: %{y}<br>Note moyenne: %{text:.1f}')
fig.update_traces(textposition='top center')
fig.update_layout(xaxis={'type': 'category'})
fig.update_layout(title={'text': 'Nombre de reviews et note moyenne par année', 'x': 0.5, 'xanchor': 'center'})
st.plotly_chart(fig, use_container_width=True)

# Affichage du DataFrame
df_grouped = data.groupby('address').agg({'rate': [('average_rate', 'mean'), ('review_count', 'count')], 'latitude': 'first', 'longitude': 'first'}).reset_index()
df_grouped.columns = ['address', 'average_rate', 'review_count', 'latitude', 'longitude']

df_grouped['average_rate'] = df_grouped['average_rate'].round(1)

fig = go.Figure(go.Scattermapbox(
    lat=df_grouped['latitude'],
    lon=df_grouped['longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=10,
        color='rgb(0, 0, 255)',
        opacity=0.7,
        cmin=df_grouped['average_rate'].min(),
        cmax=df_grouped['average_rate'].max(),
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
st.plotly_chart(fig, use_container_width=True)