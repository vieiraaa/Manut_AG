import streamlit as st
import pandas as pd
from database import (
    listar_ordens, listar_colaboradores,
    adicionar_ordem, excluir_ordem, atualizar_ordem_completa
)

st.set_page_config(page_title="Ordens de Serviço", layout="wide")
st.title("📄 Ordens de Serviço - Manutenção")

# === Dados simulados ===
tipos = ["Corretiva", "Preventiva", "Preditiva", "Inspeção", "Lubrificação", "Melhoria"]
prioridades = ["Urgente", "Alta", "Média", "Baixa"]
status_list = ["Pendente", "Aprovada", "Programada", "Iniciada", "Finalizada"]
setores = ["MDF1", "MDF2", "MDF3"]
equipamentos = ["Prensa MDF1", "Caldeira MDF1", "Prensa MDF2", "Caldeira MDF2"]
especialidades = ["MEC", "ELT"]

# === Listar colaboradores
colabs = listar_colaboradores()
df_colab = pd.DataFrame(colabs, columns=["ID", "Nome", "Especialidade", "Setor", "Jornada", "Dias"])
nomes_tecnicos = df_colab["Nome"].tolist()
ids_tecnicos = dict(zip(df_colab["Nome"], df_colab["ID"]))

# === Formulário de nova OS
with st.expander("➕ Cadastrar Nova Ordem de Serviço"):
    descricao = st.text_input("Descrição")
    tipo = st.selectbox("Tipo de Manutenção", tipos)
    setor = st.selectbox("Setor", setores)
    equipamento = st.selectbox("Equipamento", equipamentos)
    prioridade = st.selectbox("Prioridade", prioridades)
    status = st.selectbox("Status", status_list)  # Adicionado
    especialidade = st.selectbox("Especialidade", especialidades)
    duracao = st.number_input("Duração Prevista (h)", min_value=0.5, step=0.5)
    tecnicos_selecionados = st.multiselect("Técnicos Responsáveis", nomes_tecnicos)

    if st.button("Cadastrar Ordem"):
        tecnicos_ids = [ids_tecnicos[nome] for nome in tecnicos_selecionados]
        adicionar_ordem(descricao, tipo, setor, equipamento, prioridade, status, especialidade, duracao, str(tecnicos_ids))
        st.success("✅ Ordem de Serviço cadastrada com sucesso!")
        st.experimental_rerun()

st.divider()

# === Tabela de ordens
ordens = listar_ordens()
if not ordens:
    st.info("ℹ️ Nenhuma OS cadastrada ainda.")
    st.stop()

df_ordens = pd.DataFrame(ordens, columns=[
    "ID", "Descrição", "Tipo", "Setor", "Equipamento", "Prioridade",
    "Status", "Especialidade", "Duração", "Técnicos"
])
df_ordens["Técnicos"] = df_ordens["Técnicos"].fillna("[]")

# === Selecionar OS
st.subheader("📋 Ordens Cadastradas")
ordem_id = st.selectbox("Selecione uma OS para editar ou excluir:", df_ordens["ID"])

os_selecionada = df_ordens[df_ordens["ID"] == ordem_id].iloc[0]

descricao_edit = st.text_input("Descrição", os_selecionada["Descrição"])
tipo_edit = st.selectbox("Tipo de Manutenção", tipos, index=tipos.index(os_selecionada["Tipo"]))
setor_edit = st.selectbox("Setor", setores, index=setores.index(os_selecionada["Setor"]))
equipamento_edit = st.selectbox("Equipamento", equipamentos, index=equipamentos.index(os_selecionada["Equipamento"]))
prioridade_edit = st.selectbox("Prioridade", prioridades, index=prioridades.index(os_selecionada["Prioridade"]))
status_edit = st.selectbox("Status", status_list, index=status_list.index(os_selecionada["Status"]))
especialidade_edit = st.selectbox("Especialidade", especialidades, index=especialidades.index(os_selecionada["Especialidade"]))
duracao_edit = st.number_input("Duração Prevista (h)", value=float(os_selecionada["Duração"]), min_value=0.5, step=0.5)

# Técnicos da OS convertidos de string para lista
tecnicos_ids_str = os_selecionada["Técnicos"].strip("[]").split(",")
tecnicos_edit = [df_colab[df_colab["ID"] == int(t)].iloc[0]["Nome"]
                 for t in tecnicos_ids_str if t.strip().isdigit()]

tecnicos_edit = st.multiselect("Técnicos Responsáveis", nomes_tecnicos, default=tecnicos_edit)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Salvar Edição"):
        tecnicos_ids = [ids_tecnicos[nome] for nome in tecnicos_edit]
        atualizar_ordem_completa(
            ordem_id, descricao_edit, setor_edit, prioridade_edit,
            equipamento_edit, tipo_edit, duracao_edit,
            str(tecnicos_ids), status_edit, especialidade_edit
        )
        st.success("✅ Ordem atualizada com sucesso!")
        st.experimental_rerun()

with col2:
    if st.button("🗑️ Excluir Ordem"):
        excluir_ordem(ordem_id)
        st.warning("⚠️ Ordem excluída.")
        st.experimental_rerun()
