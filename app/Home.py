"""Ponto de entrada do Garimpo. Uso: streamlit run app/Home.py

So define o menu: com st.navigation os titulos podem ter acento (a pasta pages/ usaria o nome do arquivo).
"""
import streamlit as st

st.navigation([
    st.Page("busca.py", title="Busca", icon="🔎", default=True),
    st.Page("pages/1_Atualizar_catalogo.py", title="Atualizar catálogo", icon="🔄"),
    st.Page("pages/2_Adaptacoes.py", title="Adaptações", icon="🔧"),
]).run()
