import pandas as pd
import streamlit as st

st.set_page_config(page_title='France Echange', layout='wide', initial_sidebar_state='collapsed')
st.markdown("<h1 style='text-align: center;'>Indicateurs de performances du service publique de l'emploi</h1>", unsafe_allow_html=True)

df = pd.read_csv('predict_label/result_df.csv')
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
st.markdown("")
st.markdown("")
st.write("Nous utilisons les indicateurs de performance déja mise en place par le Service Publics +, afin d'apporter de la cohérence dans les outils de pilotage de la relation usagers. Ces indicateurs de performance sont :")
st.markdown(" \
        - Information/Explication \n \
        - Accessibilité\n \
        - Relation \n \
        - Réactivité \n \
        - Simplicité ")

st.markdown("") 
st.markdown("<h2 style='text-align: center;'>Indicateurs de performances</h2>", unsafe_allow_html=True)
col0, col1, col2, col3, col4, col5= st.columns(6)
with col0:
    st. metric(label="", value=f"Négatif")
    st. metric(label="", value=f"Positif")
    st. metric(label="", value=f"Neutre")
with col1:
    st.metric(label="Information/Explication", value=f"{percentage_neg_info_predicted}%")
    st.metric(label=" Information/Explication", value=f"{percentage_pos_info_predicted}%")
    st.metric(label="Information/Explication", value=f"{percentage_neutre_info_predicted}%")

with col2:
    st.metric(label=" Accessibilité", value=f"{percentage_pos_access_predicted}%")
    st.metric(label="Accessibilité", value=f"{percentage_neg_access_predicted}%")
    st.metric(label="Accessibilité", value=f"{percentage_neutre_access_predicted}%")

with col3:
    st.metric(label="Relation", value=f"{percentage_pos_relation_predicted}%")
    st.metric(label="Relation", value=f"{percentage_neg_relation_predicted}%")
    st.metric(label="Relation", value=f"{percentage_neutre_relation_predicted}%")

with col4:
    st.metric(label="Réactivité", value=f"{percentage_pos_reactivite_predicted}%")
    st.metric(label="Réactivité", value=f"{percentage_neg_reactivite_predicted}%")
    st.metric(label="Réactivité", value=f"{percentage_neutre_reactivite_predicted}%")

with col5:
    st.metric(label="Simplicité", value=f"{percentage_pos_simplicite_predicted}%")
    st.metric(label="Simplicité", value=f"{percentage_neg_simplicite_predicted}%")
    st.metric(label="Simplicité", value=f"{percentage_neutre_simplicite_predicted}%")

