import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from login import autenticar_usuario
from database import (
    listar_ordens,
    listar_colaboradores,
    limpar_programacao,
    carregar_programacao,
)
from algoritmo_genetico import executar_algoritmo_genetico
from database import inicializar_banco
inicializar_banco()

autenticar_usuario()
st.set_page_config(page_title="Programação Semanal", layout="wide")
st.title("🗓️ Programação Semanal de Manutenção")

# === Obter dados
ordens = listar_ordens()
colaboradores = listar_colaboradores()

if not ordens or not colaboradores:
    st.warning("⚠️ Cadastre ao menos uma OS e um colaborador para visualizar a programação.")
    st.stop()

# === Preparar técnicos
df_colab = pd.DataFrame(colaboradores, columns=["ID", "Nome", "Especialidade", "Setor", "Jornada", "Dias"])
tecnicos_dict = df_colab.set_index("ID")["Nome"].to_dict()

# === Datas da semana
hoje = datetime.today()
inicio_semana = hoje - timedelta(days=hoje.weekday())
dias_semana = [(inicio_semana + timedelta(days=i)).strftime("%a\n%d/%m") for i in range(7)]

# === Parâmetros configuráveis
with st.expander("⚙️ Parâmetros do Algoritmo Genético"):
    tamanho_populacao = st.number_input("Tamanho da População", min_value=10, max_value=500, value=50, step=10)
    n_geracoes = st.number_input("Número de Gerações", min_value=10, max_value=1000, value=30, step=5)
    taxa_mutacao = st.slider("Taxa de Mutação", min_value=0.0, max_value=1.0, value=0.1, step=0.05)

# === Ações
col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Limpar Programação"):
        limpar_programacao()
        st.success("✅ Programação limpa com sucesso!")
        st.rerun()

with col2:
    if st.button("⚙️ Gerar Programação com AG"):
        st.info("🔄 Executando algoritmo genético...")
        executar_algoritmo_genetico(
            tamanho_populacao=int(tamanho_populacao),
            n_geracoes=int(n_geracoes),
            taxa_mutacao=taxa_mutacao
        )
        st.success("✅ Programação gerada com sucesso!")
        st.rerun()

st.divider()

# === Exibir Programação
st.markdown("## 🗓️ Calendário Semanal Salvo no Banco")

programacao_salva = carregar_programacao()
if not programacao_salva:
    st.warning("⚠️ Nenhuma programação encontrada.")
    st.stop()

# Organizar por técnico
programacao_dict = {tec_id: {} for tec_id in tecnicos_dict.keys()}

for id_ordem, id_tecnico, data_str in programacao_salva:
    data_obj = datetime.strptime(data_str, "%Y-%m-%d")
    dia_coluna = data_obj.strftime("%a\n%d/%m")
    if dia_coluna not in programacao_dict[id_tecnico]:
        programacao_dict[id_tecnico][dia_coluna] = []
    programacao_dict[id_tecnico][dia_coluna].append(f"OS {id_ordem}")

# Exibir calendário
for tecnico_id, tecnico_nome in tecnicos_dict.items():
    st.markdown(f"### 👷 {tecnico_nome}")
    linha = {dia: "\n".join(programacao_dict[tecnico_id].get(dia, [])) for dia in dias_semana}
    tabela = pd.DataFrame([linha])
    st.dataframe(tabela, use_container_width=True, height=150)
    st.markdown("---")
