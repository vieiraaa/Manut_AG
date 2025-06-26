import streamlit as st
import pandas as pd
from database import (
    listar_ordens,
    adicionar_ordem,
    excluir_ordem,
    atualizar_ordem_completa
)

st.set_page_config(page_title="Ordens de Serviço", layout="wide")
st.title("📄 Ordens de Serviço")

# Carregar dados
ordens = listar_ordens()
df = pd.DataFrame(ordens, columns=[
    "ID", "Descrição", "Tipo", "Setor", "Equipamento", "Prioridade",
    "Status", "Especialidade", "Duração", "Técnicos"
])

st.dataframe(df, use_container_width=True)

st.divider()
st.subheader("➕ Nova Ordem de Serviço")

tipos = ["Corretiva", "Preventiva", "Preditiva", "Inspeção", "Lubrificação", "Melhoria"]
setores = ["MDF1", "MDF2", "MDF3"]
equipamentos = ["Prensa MDF1", "Caldeira MDF1", "Prensa MDF2", "Caldeira MDF2", "Prensa MDF3", "Caldeira MDF3"]
prioridades = ["Urgente", "Alta", "Média", "Baixa"]
status_opcoes = ["Pendente", "Aprovada", "Programada", "Iniciada", "Finalizada"]
especialidades = ["MEC", "ELT"]

with st.form("nova_os"):
    col1, col2, col3 = st.columns(3)
    with col1:
        descricao = st.text_input("Descrição")
        tipo = st.selectbox("Tipo de Manutenção", tipos)
        setor = st.selectbox("Setor", setores)
    with col2:
        equipamento = st.selectbox("Equipamento", equipamentos)
        prioridade = st.selectbox("Prioridade", prioridades)
        status = st.selectbox("Status", status_opcoes)
    with col3:
        especialidade = st.selectbox("Especialidade", especialidades)
        duracao = st.number_input("Duração Prevista (h)", min_value=0.5, step=0.5)
        tecnicos = st.text_input("IDs Técnicos Separados por Vírgula", help="Ex: 1,2,3")

    submitted = st.form_submit_button("Salvar")
    if submitted:
        adicionar_ordem(descricao, tipo, setor, equipamento, prioridade, status,
                        especialidade, duracao, tecnicos)
        st.success("✅ Ordem adicionada com sucesso!")
        st.experimental_rerun()

st.divider()
st.subheader("✏️ Editar ou Excluir Ordem Existente")

ids_ordens = df["ID"].tolist()
id_escolhido = st.selectbox("Selecione uma OS pelo ID", ids_ordens)

os_selecionada = df[df["ID"] == id_escolhido].iloc[0]

# Segurança nas seleções
tipo_padrao = os_selecionada["Tipo"] if os_selecionada["Tipo"] in tipos else tipos[0]
setor_padrao = os_selecionada["Setor"] if os_selecionada["Setor"] in setores else setores[0]
equip_padrao = os_selecionada["Equipamento"] if os_selecionada["Equipamento"] in equipamentos else equipamentos[0]
prioridade_padrao = os_selecionada["Prioridade"] if os_selecionada["Prioridade"] in prioridades else prioridades[0]
status_padrao = os_selecionada["Status"] if os_selecionada["Status"] in status_opcoes else status_opcoes[0]
especialidade_padrao = os_selecionada["Especialidade"] if os_selecionada["Especialidade"] in especialidades else especialidades[0]

with st.form("editar_os"):
    col1, col2, col3 = st.columns(3)
    with col1:
        desc_edit = st.text_input("Descrição", os_selecionada["Descrição"])
        tipo_edit = st.selectbox("Tipo de Manutenção", tipos, index=tipos.index(tipo_padrao))
        setor_edit = st.selectbox("Setor", setores, index=setores.index(setor_padrao))
    with col2:
        equipamento_edit = st.selectbox("Equipamento", equipamentos, index=equipamentos.index(equip_padrao))
        prioridade_edit = st.selectbox("Prioridade", prioridades, index=prioridades.index(prioridade_padrao))
        status_edit = st.selectbox("Status", status_opcoes, index=status_opcoes.index(status_padrao))
    with col3:
        especialidade_edit = st.selectbox("Especialidade", especialidades, index=especialidades.index(especialidade_padrao))
        duracao_edit = st.number_input("Duração Prevista (h)", min_value=0.5, step=0.5, value=float(os_selecionada["Duração"]))
        tecnicos_edit = st.text_input("IDs Técnicos Separados por Vírgula", os_selecionada["Técnicos"])

    col_salvar, col_excluir = st.columns([1, 1])

    if col_salvar.form_submit_button("Salvar Alterações"):
        atualizar_ordem_completa(id_escolhido, desc_edit, setor_edit, prioridade_edit,
                                 equipamento_edit, tipo_edit, duracao_edit, tecnicos_edit,
                                 status_edit, especialidade_edit)
        st.success("✅ Ordem atualizada com sucesso!")
        st.experimental_rerun()

    if col_excluir.form_submit_button("Excluir Ordem"):
        excluir_ordem(id_escolhido)
        st.warning("⚠️ Ordem excluída com sucesso.")
        st.experimental_rerun()
