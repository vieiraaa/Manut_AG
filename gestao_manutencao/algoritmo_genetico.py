import random
import sqlite3
import numpy as np

# Histórico global para gráficos
historico_fitness_global = []

def executar_algoritmo_genetico():
    global historico_fitness_global
    historico_fitness_global = []

    # === Parâmetros ===
    tamanho_populacao = 30
    n_geracoes = 20
    taxa_mutacao = 0.1

    # === Carregar dados do banco ===
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("SELECT * FROM ordens WHERE status = 'Aprovada'")
    ordens = c.fetchall()
    c.execute("SELECT * FROM colaboradores")
    colaboradores = c.fetchall()
    conn.close()

    if not ordens or not colaboradores:
        return []

    # === Estrutura auxiliar ===
    ordem_ids = [o[0] for o in ordens]
    tecnico_ids = [t[0] for t in colaboradores]

    def gerar_individuo():
        return [random.choice(tecnico_ids) for _ in ordem_ids]

    def avaliar(individuo):
        # Simulação simples: fitness = número de ordens alocadas corretamente
        return sum(1 for i, tecnico in enumerate(individuo)
                   if colaboradores[tecnico_ids.index(tecnico)][2] == ordens[i][7])  # especialidade

    def selecionar(populacao, fitnesses):
        total = sum(fitnesses)
        probs = [f / total for f in fitnesses]
        escolhidos = np.random.choice(populacao, size=2, replace=False, p=probs)
        return escolhidos[0], escolhidos[1]

    def cruzar(pai1, pai2):
        ponto = random.randint(1, len(pai1) - 1)
        return pai1[:ponto] + pai2[ponto:]

    def mutar(individuo):
        if random.random() < taxa_mutacao:
            idx = random.randint(0, len(individuo) - 1)
            individuo[idx] = random.choice(tecnico_ids)
        return individuo

    # === Inicialização ===
    populacao = [gerar_individuo() for _ in range(tamanho_populacao)]

    for geracao in range(n_geracoes):
        fitnesses = [avaliar(ind) for ind in populacao]
        nova_pop = []

        for _ in range(tamanho_populacao):
            p1, p2 = selecionar(populacao, fitnesses)
            filho = cruzar(p1, p2)
            filho = mutar(filho)
            nova_pop.append(filho)

        populacao = nova_pop

        # Salvar estatísticas
        melhor = max(fitnesses)
        media = np.mean(fitnesses)
        pior = min(fitnesses)

        historico_fitness_global.append({
            "Melhor": melhor,
            "Média": media,
            "Pior": pior
        })

    # Melhor solução final
    melhor_indice = np.argmax([avaliar(ind) for ind in populacao])
    melhor_individuo = populacao[melhor_indice]

    # Gerar programação: (id_ordem, id_tecnico, data)
    programacao = []
    from datetime import datetime, timedelta
    data_base = datetime.today()

    for i, tecnico_id in enumerate(melhor_individuo):
        data_exec = data_base + timedelta(days=i % 7)
        data_formatada = data_exec.strftime("%Y-%m-%d")
        programacao.append((ordem_ids[i], tecnico_id, data_formatada))

    return programacao