import streamlit as st
import pandas as pd
from database import (
    listar_colaboradores,
    adicionar_ordem,
    listar_ordens,
    excluir_ordem,
    atualizar_ordem_completa
)
from login import autenticar_usuario

autenticar_usuario()

st.set_page_config(page_title="Ordens de Serviço", layout="wide")
st.title("📄 Gestão de Ordens de Serviço")

# === Dados para seleção ===
colaboradores = listar_colaboradores()
colab_dict = {f"{c[1]} (ID {c[0]})": c[0] for c in colaboradores}

setores = ["MDF1", "MDF2", "MDF3"]
prioridades = ["Urgente", "Alta", "Média", "Baixa"]
tipos_manutencao = ["Corretiva", "Preventiva", "Preditiva", "Melhoria", "Inspeção", "Lubrificação"]
especialidades = ["MEC", "ELT"]

# === Cadastro de OS ===
st.subheader("➕ Cadastrar nova Ordem de Serviço")

with st.form("form_os"):
    descricao = st.text_area("Descrição da OS")
    setor = st.selectbox("Setor", setores)
    prioridade = st.selectbox("Prioridade", prioridades)
    equipamento = st.text_input("Equipamento")
    tipo_manutencao = st.selectbox("Tipo de Manutenção", tipos_manutencao)
    especialidade = st.selectbox("Especialidade", especialidades)
    duracao_prevista = st.number_input("Duração Prevista (horas)", min_value=1.0, step=0.5)

    tecnicos_selecionados = st.multiselect(
        "👷 Técnicos Responsáveis (mínimo 1)",
        options=list(colab_dict.keys())
    )

    submitted = st.form_submit_button("Salvar OS")

    if submitted:
        if descricao == "" or equipamento == "" or len(tecnicos_selecionados) == 0:
            st.error("❌ Preencha todos os campos obrigatórios.")
        else:
            tecnicos_ids = [colab_dict[t] for t in tecnicos_selecionados]

            adicionar_ordem(
                descricao, tipo_manutencao, setor, equipamento, prioridade,
                "Pendente", especialidade, duracao_prevista, str(tecnicos_ids)
            )

            st.success("✅ Ordem cadastrada com sucesso.")
            st.rerun()

# === Visualização de OS cadastradas ===
st.subheader("📋 Ordens de Serviço Cadastradas")

ordens = listar_ordens()
if ordens:
    df = pd.DataFrame(ordens, columns=[
        "ID", "Descrição", "Tipo Manutenção", "Setor", "Equipamento", "Prioridade",
        "Status", "Especialidade", "Duração (h)", "Técnicos"
    ])
    
    st.dataframe(df, use_container_width=True)

    selected_index = st.selectbox("🔎 Selecione uma OS para ação:", df["ID"])

    os = df[df["ID"] == selected_index].iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✏️ Editar OS"):
            st.markdown("### 🛠️ Editar Ordem de Serviço")
            with st.form("form_editar_os"):
                descricao = st.text_area("Descrição", value=os["Descrição"])
                setor = st.selectbox("Setor", setores, index=setores.index(os["Setor"]))
                prioridade = st.selectbox("Prioridade", prioridades, index=prioridades.index(os["Prioridade"]))
                equipamento = st.text_input("Equipamento", value=os["Equipamento"])
                tipo_manutencao = st.selectbox("Tipo de Manutenção", tipos_manutencao, index=tipos_manutencao.index(os["Tipo Manutenção"]))
                especialidade = st.selectbox("Especialidade", especialidades, index=especialidades.index(os["Especialidade"]))
                duracao = st.number_input("Duração Prevista (horas)", min_value=1.0, step=0.5, value=float(os["Duração (h)"]))
                status = st.selectbox("Status", ["Pendente", "Aprovada", "Programada", "Iniciada", "Finalizada"], index=0)
                tecnicos = st.text_input("IDs dos Técnicos (ex: [1,2])", value=os["Técnicos"])

                if st.form_submit_button("Salvar Alterações"):
                    atualizar_ordem_completa(
                        os["ID"], descricao, setor, prioridade, equipamento,
                        tipo_manutencao, duracao, tecnicos, status, especialidade
                    )
                    st.success("✅ Ordem atualizada com sucesso.")
                    st.rerun()

    with col2:
        if st.button("🗑️ Excluir OS"):
            excluir_ordem(int(selected_index))
            st.warning(f"⚠️ Ordem {selected_index} excluída.")
            st.rerun()

    with col3:
        if st.button("📄 Criar Cópia"):
            adicionar_ordem(
                os["Descrição"], os["Tipo Manutenção"], os["Setor"], os["Equipamento"],
                os["Prioridade"], "Pendente", os["Especialidade"],
                os["Duração (h)"], os["Técnicos"]
            )
            st.success("✅ Cópia criada com sucesso.")
            st.rerun()

else:
    st.warning("⚠️ Nenhuma OS cadastrada ainda.")
