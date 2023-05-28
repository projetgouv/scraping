import streamlit as st
import pandas as pd
st.set_page_config(page_title='France Echanges', layout='wide')


# Titre
st.markdown("<h1 style='text-align: center;'>🇫🇷 France Échanges construisons ensemble France Travail</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>France Échanges, un projet innovant qui vise à améliorer les services publics de l'emploi et de l'insertion professionnelle</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.error("Ce projet est réalisé dans le cadre d'un partenariat pégagogique entre Service Public + et HETIC. L'entité France Echanges est fictive et les données utilisées sont des données publiques.", icon='⛔️')
st.warning("Nous avons rencontré quelques problèmes techniques, avec des données qui n'ont pas été intégralement extraites lors du scraping.", icon='ℹ️')

st.markdown("<br>", unsafe_allow_html=True)
st.write("Dans la lignée du Service Public +, où l'innovation technologique et l'utilisation des données sont au cœur du progrès des insitutions, le projet novateur **France Échanges** exploite les avis Google déposés sur les fiches Pôle Emploi. Grâce à des techniques de traitement automatique du langage naturel (NLP), nous analysons les commentaires des utilisateurs afin de comprendre leur verbatim, de mettre en évidence les reproches fréquents et d'identifier les aspects qui fonctionnent bien et ceux qui posent problème.")
st.write("Pour mener à bien ce projet, nous utilisons des technologies avancées de NLP: l'**analyse des sentiments** et **topic modelling**  (BERTopic). Nous utilisons également la **visualisation de données** pour présenter les résultats de notre analyse.")
