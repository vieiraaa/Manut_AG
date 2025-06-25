import sqlite3

# Conecta (ou cria) o banco de dados
conn = sqlite3.connect("manutencao.db")
cursor = conn.cursor()

# === TABELA DE COLABORADORES ===
cursor.execute("""
CREATE TABLE IF NOT EXISTS colaboradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    especialidade TEXT NOT NULL,
    setor TEXT NOT NULL,
    jornada TEXT,
    dias_disponiveis TEXT
);
""")

# Inserção de colaboradores fictícios
colaboradores = [
    ("Pedro", "MEC", "MDF1", "08h-18h", "Segunda a Sexta"),
    ("Paulo", "MEC", "MDF1", "08h-18h", "Segunda a Sexta"),
    ("João", "ELT", "MDF1", "08h-18h", "Segunda a Sexta"),
    ("Jonas", "ELT", "MDF1", "08h-18h", "Segunda a Sexta")
]

for c in colaboradores:
    cursor.execute("""
        INSERT INTO colaboradores (nome, especialidade, setor, jornada, dias_disponiveis)
        VALUES (?, ?, ?, ?, ?)
    """, c)

# === TABELA DE ORDENS DE SERVIÇO ===
cursor.execute("""
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
);
""")

conn.commit()
conn.close()

print("✅ Banco de dados inicializado com sucesso!")


conn = sqlite3.connect("manutencao.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS programacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_ordem INTEGER NOT NULL,
    id_tecnico INTEGER NOT NULL,
    data TEXT NOT NULL
);
""")

conn.commit()
conn.close()

print("✅ Tabela 'programacao' criada com sucesso.")