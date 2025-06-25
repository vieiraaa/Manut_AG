import streamlit as st
from login import autenticar_usuario

st.set_page_config(page_title="Sistema de Manutenção", layout="wide")

autenticar_usuario()

st.title("🏭 Sistema de Gestão de Manutenção")
st.markdown("Use o menu lateral para navegar entre as funcionalidades.")
