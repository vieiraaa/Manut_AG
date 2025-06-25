import streamlit as st
import pandas as pd
from login import autenticar_usuario
from database import listar_colaboradores, adicionar_colaborador, atualizar_colaborador, excluir_colaborador
from database import inicializar_banco
inicializar_banco()

autenticar_usuario()

st.set_page_config(page_title="Colaboradores", layout="wide")
st.title("👷 Cadastro e Consulta de Colaboradores")

# === Cadastro de novo colaborador ===
st.subheader("➕ Cadastrar novo colaborador")

with st.form("form_colab"):
    nome = st.text_input("Nome")
    especialidade = st.selectbox("Especialidade", ["MEC", "ELT"])
    setor = st.selectbox("Setor", ["MDF1", "MDF2", "MDF3"])
    jornada = st.text_input("Jornada (ex: 08h-18h)")
    dias = st.text_input("Dias disponíveis (ex: Segunda a Sexta)")

    submitted = st.form_submit_button("Salvar Colaborador")
    if submitted:
        if nome.strip() == "":
            st.error("❌ Nome é obrigatório.")
        else:
            adicionar_colaborador(nome, especialidade, setor, jornada, dias)
            st.success("✅ Colaborador cadastrado com sucesso.")
            st.rerun()

# === Visualização de colaboradores ===
st.subheader("📋 Colaboradores Cadastrados")

dados = listar_colaboradores()

if dados:
    df = pd.DataFrame(dados, columns=["ID", "Nome", "Especialidade", "Setor", "Jornada", "Dias Disponíveis"])

    selected_id = st.selectbox("🔎 Selecione um colaborador para ação:", df["ID"])
    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✏️ Editar"):
            colab = df[df["ID"] == selected_id].iloc[0]
            st.markdown("### 🛠️ Editar Colaborador")
            with st.form("form_edit_colab"):
                nome = st.text_input("Nome", value=colab["Nome"])
                especialidade = st.selectbox("Especialidade", ["MEC", "ELT"], index=["MEC", "ELT"].index(colab["Especialidade"]))
                setor = st.selectbox("Setor", ["MDF1", "MDF2", "MDF3"], index=["MDF1", "MDF2", "MDF3"].index(colab["Setor"]))
                jornada = st.text_input("Jornada", value=colab["Jornada"])
                dias = st.text_input("Dias disponíveis", value=colab["Dias Disponíveis"])

                if st.form_submit_button("Salvar Alterações"):
                    atualizar_colaborador(colab["ID"], nome, especialidade, setor, jornada, dias)
                    st.success("✅ Alterações salvas.")
                    st.rerun()

    with col2:
        if st.button("🗑️ Excluir"):
            excluir_colaborador(int(selected_id))
            st.warning("⚠️ Colaborador excluído.")
            st.rerun()

    with col3:
        if st.button("📄 Criar Cópia"):
            colab = df[df["ID"] == selected_id].iloc[0]
            adicionar_colaborador(colab["Nome"], colab["Especialidade"], colab["Setor"], colab["Jornada"], colab["Dias Disponíveis"])
            st.success("✅ Cópia criada.")
            st.rerun()

else:
    st.warning("⚠️ Nenhum colaborador cadastrado ainda.")
