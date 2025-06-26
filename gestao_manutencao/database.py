import sqlite3

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

# database.py

def inicializar_banco():
    conn = sqlite3.connect("banco_dados.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS colaboradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            especialidade TEXT,
            setor TEXT,
            jornada INTEGER,
            dias TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS ordens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            tipo_manutencao TEXT,
            setor TEXT,
            equipamento TEXT,
            prioridade TEXT,
            status TEXT,
            especialidade TEXT,
            duracao_prevista REAL,
            tecnicos TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS programacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_ordem INTEGER,
            id_tecnico INTEGER,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()
