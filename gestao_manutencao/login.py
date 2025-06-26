import streamlit as st

def autenticar_usuario():
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("🔐 Lodasdsadasdsagin")

        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if usuario == "admin" and senha == "1234":  # Trocar no futuro
                st.session_state.autenticado = True
                st.experimental_rerun()
            else:
                st.error("Credenciais inválidas")

        st.stop()
