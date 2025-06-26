import random
import sqlite3
import numpy as np
from datetime import datetime, timedelta

# Histórico global para gráficos
historico_fitness_global = []

def listar_ordens():
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("SELECT * FROM ordens")
    resultado = c.fetchall()
    conn.close()
    return resultado

def listar_colaboradores():
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("SELECT * FROM colaboradores")
    resultado = c.fetchall()
    conn.close()
    return resultado

def adicionar_ordem(descricao, tipo_manutencao, setor, equipamento, prioridade, status, especialidade, duracao_prevista, tecnicos):
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO ordens (descricao, tipo_manutencao, setor, equipamento, prioridade, status, especialidade, duracao_prevista, tecnicos)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (descricao, tipo_manutencao, setor, equipamento, prioridade, status, especialidade, duracao_prevista, tecnicos))
    conn.commit()
    conn.close()

def excluir_ordem(id_ordem):
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("DELETE FROM ordens WHERE id = ?", (id_ordem,))
    conn.commit()
    conn.close()

def atualizar_ordem_completa(id_ordem, descricao, setor, prioridade, equipamento, tipo_manutencao, duracao_prevista, tecnicos, status, especialidade):
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("""
        UPDATE ordens SET descricao=?, setor=?, prioridade=?, equipamento=?, tipo_manutencao=?,
        duracao_prevista=?, tecnicos=?, status=?, especialidade=? WHERE id=?
    """, (descricao, setor, prioridade, equipamento, tipo_manutencao, duracao_prevista, tecnicos, status, especialidade, id_ordem))
    conn.commit()
    conn.close()

def limpar_programacao():
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("DELETE FROM programacao")
    conn.commit()
    conn.close()

def carregar_programacao():
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("SELECT id_ordem, id_tecnico, data FROM programacao")
    resultado = c.fetchall()
    conn.close()
    return resultado

def adicionar_colaborador(nome, especialidade, setor, jornada, dias):
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO colaboradores (nome, especialidade, setor, jornada, dias)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, especialidade, setor, jornada, dias))
    conn.commit()
    conn.close()

def atualizar_colaborador(id_colab, nome, especialidade, setor, jornada, dias):
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("""
        UPDATE colaboradores SET nome=?, especialidade=?, setor=?, jornada=?, dias=? WHERE id=?
    """, (nome, especialidade, setor, jornada, dias, id_colab))
    conn.commit()
    conn.close()

def excluir_colaborador(id_colab):
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("DELETE FROM colaboradores WHERE id = ?", (id_colab,))
    conn.commit()
    conn.close()

def executar_algoritmo_genetico(tamanho_populacao=50, n_geracoes=30, taxa_mutacao=0.1):
    global historico_fitness_global
    historico_fitness_global = []

    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("SELECT * FROM ordens WHERE status = 'Aprovada'")
    ordens = c.fetchall()
    c.execute("SELECT * FROM colaboradores")
    colaboradores = c.fetchall()
    conn.close()

    if not ordens or not colaboradores:
        return []

    ordem_ids = [o[0] for o in ordens]
    tecnico_ids = [t[0] for t in colaboradores]

    def gerar_individuo():
        return [random.choice(tecnico_ids) for _ in ordem_ids]

    def avaliar(individuo):
        return sum(1 for i, tecnico in enumerate(individuo)
                   if colaboradores[tecnico_ids.index(tecnico)][2] == ordens[i][7])

    def selecionar(populacao, fitnesses):
        total = sum(fitnesses)
        if total == 0:
            probs = [1 / len(fitnesses)] * len(fitnesses)
        else:
            probs = [f / total for f in fitnesses]
        escolhidos = np.random.choice(len(populacao), size=2, replace=False, p=probs)
        return populacao[escolhidos[0]], populacao[escolhidos[1]]

    def cruzar(pai1, pai2):
        ponto = random.randint(1, len(pai1) - 1)
        return pai1[:ponto] + pai2[ponto:]

    def mutar(individuo):
        if random.random() < taxa_mutacao:
            idx = random.randint(0, len(individuo) - 1)
            individuo[idx] = random.choice(tecnico_ids)
        return individuo

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

        melhor = max(fitnesses)
        media = np.mean(fitnesses)
        pior = min(fitnesses)

        historico_fitness_global.append({
            "Melhor": melhor,
            "Média": media,
            "Pior": pior
        })

    melhor_indice = np.argmax([avaliar(ind) for ind in populacao])
    melhor_individuo = populacao[melhor_indice]

    programacao = []
    data_base = datetime.today()

    for i, tecnico_id in enumerate(melhor_individuo):
        data_exec = data_base + timedelta(days=i % 7)
        data_formatada = data_exec.strftime("%Y-%m-%d")
        programacao.append((ordem_ids[i], tecnico_id, data_formatada))

    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("DELETE FROM programacao")
    c.executemany("INSERT INTO programacao (id_ordem, id_tecnico, data) VALUES (?, ?, ?)", programacao)
    conn.commit()
    conn.close()

    return programacao
