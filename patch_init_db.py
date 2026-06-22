import re

with open('backend/database.py', 'r') as f:
    content = f.read()

# Replace CREATE TABLE historico_leitura to include codigo_projeto
new_historico = """        CREATE TABLE IF NOT EXISTS historico_leitura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT,
            umidade REAL,
            temperatura_max REAL,
            temperatura_min REAL,
            status_solo TEXT,
            tempo_irrigacao_calculado REAL,
            eto_calculada REAL,
            cad_calculada REAL,
            irn_calculada REAL,
            comprimento_lateral_m REAL,
            perda_carga_total_mca REAL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""

content = re.sub(
    r"CREATE TABLE IF NOT EXISTS historico_leitura \([\s\S]*?data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n\s*\)",
    new_historico,
    content
)

# We also need to add ALTER TABLE snippet
alter_table_snippet = """    cursor.execute("PRAGMA table_info(historico_leitura)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'codigo_projeto' not in columns:
        cursor.execute('ALTER TABLE historico_leitura ADD COLUMN codigo_projeto TEXT')"""

# Insert alter table right after creating the table
content = content.replace("    cursor.execute('''\n        CREATE TABLE IF NOT EXISTS culturas", alter_table_snippet + "\n    cursor.execute('''\n        CREATE TABLE IF NOT EXISTS culturas")

with open('backend/database.py', 'w') as f:
    f.write(content)
