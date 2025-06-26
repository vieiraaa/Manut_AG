import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from algoritmo_genetico import historico_fitness_global  # Deve estar visível no módulo
from database import inicializar_banco
inicializar_banco()

st.set_page_config(page_title="Indicadores de Manutenção", layout="wide")
st.title("📈 Indicadores de Desempenho - Manutenção Industrial")

# === KPIs Simulados ===
mttr = 3.4
mtbf = 42.7
backlog = 128.5
cumprimento_planejado = 82.3

col1, col2, col3, col4 = st.columns(4)
col1.metric("🛠️ MTTR", f"{mttr} h", "-0.2 h")
col2.metric("⚙️ MTBF", f"{mtbf} h", "+1.5 h")
col3.metric("📋 Backlog", f"{backlog} h", "+5.2 h")
col4.metric("📅 Cumprimento Planejado", f"{cumprimento_planejado}%", "-3.1%")

st.divider()

# === Gráfico de OSs por tipo (REAL) ===
st.subheader("Distribuição de Ordens de Manutenção por Tipo")

conn = sqlite3.connect("banco_dados.db")
c = conn.cursor()
c.execute("SELECT tipo_manutencao, COUNT(*) FROM ordens GROUP BY tipo_manutencao")
dados_tipos = c.fetchall()
conn.close()

if dados_tipos:
    df_tipos = pd.DataFrame(dados_tipos, columns=["Tipo", "Quantidade"])
    fig = px.bar(df_tipos, x="Tipo", y="Quantidade", color="Tipo", title="Ordens por Tipo (Base Real)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("ℹ️ Nenhuma ordem de manutenção cadastrada no momento.")


# === Backlog semanal ===
st.subheader("Evolução do Backlog nas Últimas Semanas")
semanas = ["S1", "S2", "S3", "S4", "S5"]
backlog_sem = [152, 138, 125, 122, 128]
df_backlog = pd.DataFrame({"Semana": semanas, "Backlog (h)": backlog_sem})
fig_backlog = px.line(df_backlog, x="Semana", y="Backlog (h)", markers=True, title="Backlog Histórico")
st.plotly_chart(fig_backlog, use_container_width=True)

st.divider()

# === Histórico do Algoritmo Genético ===
st.subheader("📊 Histórico de Fitness - Algoritmo Genético")

if not historico_fitness_global:
    st.warning("⚠️ Execute o algoritmo genético para visualizar os gráficos de fitness.")
else:
    df_fit = pd.DataFrame(historico_fitness_global).reset_index().rename(columns={"index": "Geração"})

    st.markdown("#### 📈 Evolução do Fitness (linha)")
    fig_fit_line = px.line(df_fit, x="Geração", y=["Melhor", "Média", "Pior"], markers=True)
    st.plotly_chart(fig_fit_line, use_container_width=True)

    st.markdown("#### 📦 Distribuição do Fitness por Geração (boxplot)")
    df_melt = df_fit.melt(id_vars="Geração", var_name="Tipo", value_name="Fitness")
    fig_fit_box = px.box(df_melt, x="Geração", y="Fitness", color="Tipo", points="outliers")
    st.plotly_chart(fig_fit_box, use_container_width=True)

st.caption("Todos os dados são simulados ou em memória para fins de apresentação.")
