import streamlit as st
import pandas as pd
st.set_page_config(page_title='France Echange', layout='wide', initial_sidebar_state='collapsed')
st.markdown("<h1 style='text-align: center;'>France Echange construisons ensemble le service publique de l'emploi</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.error("Ce projet est réalisé dans le cadre d'un partenariat pégagogique entre Service Public + et HETIC. L'entité France Echange est fictive et les données utilisées sont des données publiques.", icon='⛔️')
st.warning("Nous avons rencontré quelques problèmes techniques,la données n'est pas exhaustive.", icon='ℹ️')
st.markdown("<br>", unsafe_allow_html=True)
st.write("Dans la lignée du Service Public +, où l'innovation technologique et l'utilisation des données sont au cœur du progrès des insitutions, le projet novateur **France Echange** exploite les avis Google déposés sur les fiches Pôle Emploi. Grâce à des techniques de traitement automatique du langage naturel (NLP), nous analysons les commentaires des utilisateurs afin de comprendre leur verbatim, de mettre en évidence les reproches fréquents et d'identifier les aspects qui fonctionnent bien et ceux qui posent problème.")
st.write("France Echange repose sur des techniques de traitement automatique du langage naturel (NLP) avancées, notamment l'analyse des sentiments et le topic modelling avec BERTopic. Grâce à ces outils, nous sommes en mesure d'analyser les commentaires des utilisateurs sur les fiches Pôle Emploi, ce qui nous permet de comprendre leur verbatim, de détecter les reproches fréquents, et d'identifier les aspects qui fonctionnent bien et ceux qui posent problème.")
st.write("L'emploi et l'insertion sont des enjeux majeurs pour notre société, et en exploitant les avis Google, nous pouvons obtenir des informations précieuses sur les besoins et les préoccupations des utilisateurs du service public de l'emploi. Cette analyse approfondie nous permettra de prendre des décisions plus éclairées et d'améliorer les politiques et les services liés à l'emploi et à l'insertion.")
st.write("Nous sommes conscients que ce projet rencontre quelques problèmes techniques, et nous tenons à vous informer que les données utilisées ne sont pas exhaustives. Cependant, nous sommes déterminés à surmonter ces difficultés pour offrir un service public de l'emploi plus performant et adapté aux besoins des citoyens.")
st.write("En utilisant également la visualisation de données, nous serons en mesure de présenter les résultats de manière claire et compréhensible. Cela nous permettra de communiquer efficacement avec les parties prenantes, de partager les insights obtenus et de faciliter la prise de décision.")
st.write("Nous vous remercions de votre compréhension et de votre confiance.")

col1, col2, col3 = st.columns([1, 1, 1])
col2.image('images/france-echange-low-resolution-color-logo.png', width=400)
