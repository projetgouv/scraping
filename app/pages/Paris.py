import streamlit as st
from streamlit import components
import pandas as pd
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta
from data_prep import DataProcessor, Classement

st.set_page_config(page_title='France Echanges', page_icon=':house:', layout='wide')
st.markdown("<h1 style='text-align: center;'>EDA sur les notes</h1>", unsafe_allow_html=True)
st.write("Bienvenue sur France Echanges, Ensemble, construisons le service public de l'emploi du futur en donnant la parole aux usagers")

# Load data
data_path = 'Data/google_reviews.csv'

columns = ['date', 'rate', 'review_text', 'object_address']

processor = DataProcessor(data_path)
processor.process_data(columns)
data = processor.data
#Load data2
location_path = 'Data/location.csv'
# Vous pouvez accéder aux données transformées via l'attribut `data` de l'objet `proc ssor`


classment = Classement(data_path, location_path)
classment.load_data()  # Charger les données
classment.load_location_data()  # Charger les données de localisation

# Calculer et afficher la valeur max_rate
result_max_rate = classment.max_rate()
result_min_rate = classment.min_rate() 


# Calculer le nombre de reviews, la note moyenne, la note la plus basse et la note la plus haute par année
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

# Filter out reviews for year 2013
filtered_reviews = nb_reviews[nb_reviews['years'] != '2013']

# Find the year with the highest average rating
best_year = filtered_reviews['years'][filtered_reviews['note moyenne'].idxmax()]
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Nombre de reviews", value=nb_reviews['nombre de reviews'].sum())
    st.metric(label="Année avec la meilleure note moyenne", value=best_year)
def max_mean(classment):
    max_rate_df = classment.max_rate().reset_index()
    max_rate_addresses = max_rate_df['object_address']
    max_rate_notes = max_rate_df['rate']
    name_string = ', '.join(max_rate_addresses.astype(str))
    name_string = name_string.replace('Pole emploi', ' ')
    max_rate_note = max_rate_notes.item()
    return name_string,max_rate_note

with col2:
        st.metric(label="Note moyenne", value=nb_reviews['note moyenne'].mean().round(1))
        st.write(
                """
                <style>
                [data-testid="stMetricDelta"] svg {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
        name_string, max_rate_note = max_mean(classment) 
        st.metric(label="Lieux avec la note la plus haute", value=name_string, delta=max_rate_note)
def min_mean(classment):
    min_rate_df = classment.min_rate().reset_index()
    min_rate_addresses = min_rate_df['object_address']
    min_rate_notes = min_rate_df['rate'].round(1)
    name_string = ', '.join(min_rate_addresses.astype(str))
    name_string = name_string.replace('Pole emploi', ' ')
    min_rate_note = min_rate_notes.item()
    return name_string,min_rate_note

with col3:
    st.metric(label="Nombre moyen de reviews par an", value=nb_reviews['nombre de reviews'].mean().round(1))
    st.write(
                """
                <style>
                [data-testid="stMetricDelta"] svg {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
    name_string, min_rate_note = min_mean(classment) 
    st.metric(label="Lieux avec la note la plus haute", value=name_string, delta=min_rate_note, delta_color="inverse")

st.plotly_chart(fig, use_container_width=True)

