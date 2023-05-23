import streamlit as st
import pandas as pd
from data_prep import DataProcessor
st.set_page_config(page_title='France Echanges', page_icon=':house:', layout='wide')

st.markdown("<h1 style='text-align: center;'>France Echanges</h1>", unsafe_allow_html=True)

st.write("Bienvenue sur France Echanges, Ensemble, construisons le service public de l'emploi du futur en donnant la parole aux usagers")
st.write("Nous avons rencontré quelques problèmes techniques, avec des données qui ne se sont pas chargées, vous trouvez ci-dessous une analyse des données qui ont pu être chargées")

data_file = 'all_data/google_reviews_RGPD.csv'
df_scraped_data = pd.read_csv(data_file)
columns = ['date', 'rate', 'review_text', 'object_address']
data_path = data_file
# Obtenir le nombre de lieux scrappés
nombre_lieux_scrappes = len(df_scraped_data['object_address'].unique())

# Afficher le nombre de lieux scrappés

# Charger le fichier CSV contenant les adresses
addresses_file = 'all_data/pole_emploi.csv'
df_addresses = pd.read_csv(addresses_file)
nombre_lieux = len(df_addresses['Adresse'].unique())
pourcentage_scrappes = round((nombre_lieux_scrappes / nombre_lieux) * 100, 2)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Nombre de lieux scrappés", value=nombre_lieux_scrappes)
with col2:
    st.metric(label="Nombre de lieux", value=nombre_lieux)
with col3:
    st.metric(label="Pourcentage de lieux scrappés", value=pourcentage_scrappes)
processor = DataProcessor(data_path)
processor.process_data(columns)
data = processor.data
st.dataframe(data)
nb_reviews = data.groupby('years').agg({'rate': ['count', 'mean']}).reset_index()
nb_reviews.columns = ['years', 'nombre de reviews', 'note moyenne']
nb_reviews['note moyenne'] = nb_reviews['note moyenne'].round(1)
# Créer un graphique avec l'année, le nombre de reviews et la note moyenne
fig = px.line(nb_reviews, x='years', y='nombre de reviews', text='note moyenne')
fig.update_traces(
                  hovertemplate='Année: %{x}<br>Nombre de reviews: %{y}<br>Note moyenne: %{text:.1f}')
#fig.update_layout(hovermode="x unified")
fig.update_traces(textposition='top center')
#fig.update_traces(mode="markers+lines")
fig.update_layout(xaxis={'type': 'category'})
fig.update_layout(title={'text': 'Nombre de reviews et note moyenne par année', 'x': 0.5, 'xanchor': 'center'})

st.altair_chart(fig, use_container_width=True)
