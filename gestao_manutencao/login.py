import streamlit as st

import streamlit as st

def autenticar_usuario():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        with st.form("login_form"):
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            enviar = st.form_submit_button("Entrar")

            if enviar:
                if usuario == "admin" and senha == "admin123":  # exemplo fixo
                    st.session_state.autenticado = True
                    st.success("Login bem-sucedido!")
                    st.experimental_rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
    else:
        st.sidebar.success("✅ Logado como admin")

