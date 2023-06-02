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


with st.expander("Accuracy"):
    code = """
    Processing pos_info comments...
Test accuracy for pos_info is 0.9135451240714398


Processing neg_info comments...
Test accuracy for neg_info is 0.7521732258574364


Processing neutre_info comments...
Test accuracy for neutre_info is 0.9878299351983563


Processing unknown_info comments...
Test accuracy for unknown_info is 0.6941678520625889


Processing pos_access comments...
Test accuracy for pos_access is 0.8637584953374428


Processing neg_access comments...
Test accuracy for neg_access is 0.7698751382961909


Processing neutre_access comments...
Test accuracy for neutre_access is 0.9811917180338233


Processing unknown_access comments...
Test accuracy for unknown_access is 0.7486960644855382


Processing pos_relation comments...
Test accuracy for pos_relation is 0.9227121858700806


Processing neg_relation comments...
Test accuracy for neg_relation is 0.9307728781412992


Processing neutre_relation comments...
Test accuracy for neutre_relation is 0.9951003635214162


Processing unknown_relation comments...
Test accuracy for unknown_relation is 0.8770349296665086


Processing pos_reactivite comments...
Test accuracy for pos_reactivite is 0.9359886201991465


Processing neg_reactivite comments...
Test accuracy for neg_reactivite is 0.8400505768926821


Processing neutre_reactivite comments...
Test accuracy for neutre_reactivite is 0.9952584163110479


Processing unknown_reactivite comments...
Test accuracy for unknown_reactivite is 0.7889995258416311


Processing pos_simplicite comments...
Test accuracy for pos_simplicite is 0.9173383910226015


Processing neg_simplicite comments...
Test accuracy for neg_simplicite is 0.6954322743796428


Processing neutre_simplicite comments...
Test accuracy for neutre_simplicite is 0.9876718824087245


Processing unknown_simplicite comments...
Test accuracy for unknown_simplicite is 0.6691955113007745
    """
    st.code(code, language='text')
