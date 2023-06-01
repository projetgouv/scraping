import pandas as pd
import streamlit as st

st.set_page_config(page_title='France Echange', layout='wide', initial_sidebar_state='collapsed')
st.markdown("<h1 style='text-align: center;'>KPIs nationale selon Service Public + </h1>", unsafe_allow_html=True)

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

st.dataframe(df)