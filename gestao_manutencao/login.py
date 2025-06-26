import streamlit as st

def autenticar_usuario():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("🔐 Login")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        botao = st.button("Entrar")

        if botao:
            if usuario == "admin" and senha == "1234":
                st.session_state.autenticado = True
                st.success("Login bem-sucedido!")
                st.experimental_set_query_params(logged="true")
                st.switch_page("pages/1_📄_Ordens_de_Servico.py")  # Ou qualquer página inicial
            else:
                st.error("Usuário ou senha incorretos.")
        st.stop()
