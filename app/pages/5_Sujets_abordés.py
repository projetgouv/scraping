import streamlit as st

st.set_page_config(page_title='France Echange', layout='wide', initial_sidebar_state='collapsed')
st.markdown("<h1 style='text-align: center;'>Les grands sujets nationaux</h1>", unsafe_allow_html=True)
st.write('Le Topic Modeling sert à identifier les grands sujets abordés dans les avis. Pour cela, nous avons utilisé la méthode BERTopic qui permet de faire du Topic Modeling avec des phrases et non des mots. Cela permet d\'avoir des sujets plus précis et plus pertinents.')
st.write('Nous avons donc appliqué cette méthode sur les avis et nous avons obtenu les résultats suivants :')
st.markdown("<br>", unsafe_allow_html=True)
col_pos, col_neg = st.columns(2)
col_pos.markdown("<h2 style='text-align: center;'>Les sujets positifs</h2>", unsafe_allow_html=True)
col_pos.image('topic/pos_nat.png', use_column_width=True)
col_neg.markdown("<h2 style='text-align: center;'>Les sujets négatifs</h2>", unsafe_allow_html=True)
col_neg.image('topic/neg_nat.png', use_column_width=True)
