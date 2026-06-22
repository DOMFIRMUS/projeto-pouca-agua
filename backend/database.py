import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'pouca_agua.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico_leitura (
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
        )
    ''')
    cursor.execute("PRAGMA table_info(historico_leitura)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'codigo_projeto' not in columns:
        cursor.execute('ALTER TABLE historico_leitura ADD COLUMN codigo_projeto TEXT')
    cursor.execute("PRAGMA table_info(historico_leitura)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'codigo_projeto' not in columns:
        cursor.execute('ALTER TABLE historico_leitura ADD COLUMN codigo_projeto TEXT')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS culturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            kc_inicial REAL,
            kc_media REAL,
            kc_final REAL,
            data_plantio TEXT,
            dias_fase_inicial INTEGER,
            dias_meia_estacao INTEGER,
            dias_fase_final INTEGER,
            min_ce REAL DEFAULT 1.0,
            max_ce REAL DEFAULT 3.0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projetos_metadados (
            codigo_projeto TEXT PRIMARY KEY UNIQUE,
            nome_projeto TEXT,
            nome_propriedade TEXT,
            nome_proprietario TEXT,
            nome_projetista TEXT,
            codigo_subunidade TEXT,
            area_total_irrigada REAL,
            area_subunidade REAL,
            data_elaboracao TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projetos_metadados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT UNIQUE NOT NULL,
            nome_projeto TEXT,
            nome_propriedade TEXT,
            nome_proprietario TEXT,
            nome_projetista TEXT,
            identificacao TEXT,
            nome_codigo_subunidade TEXT,
            area_total_irrigada REAL,
            area_subunidade REAL,
            data_elaboracao TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            taxa_mensal REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projetos_metadados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT UNIQUE NOT NULL,
            nome_projeto TEXT,
            largura INTEGER,
            altura INTEGER,
            profundidade INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_projeto_metadados(codigo_projeto, nome_projeto, largura, altura, profundidade):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO projetos_metadados (codigo_projeto, nome_projeto, largura, altura, profundidade)
            VALUES (?, ?, ?, ?, ?)
        ''', (codigo_projeto, nome_projeto, largura, altura, profundidade))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Retorna False se houver violação da constraint UNIQUE do codigo_projeto
        return False
    finally:
        conn.close()

def get_projeto_metadados(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def seed_culturas():
    conn = get_db_connection()
    cursor = conn.cursor()

    culturas = [
        ('Algodoeiro', 0.35, 1.20, 0.60, '2023-10-01', 30, 50, 40, 7.7, 27.0),
        ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30, 1.7, 10.0),
        ('Tomate', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 2.5, 12.5),
        ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15, 1.3, 4.0),
        ('Cebola', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.2, 7.2),
        ('Tomate tutorado', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 1.0, 3.0),
        ('Batata', 0.50, 1.15, 0.75, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Cebola seca', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.0, 3.0),
        ('Melancia', 0.40, 1.00, 0.75, '2023-09-05', 20, 30, 20, 1.0, 3.0),
        ('Melão', 0.50, 1.05, 0.75, '2023-09-05', 20, 30, 20, 1.0, 3.0),
        ('Pepino', 0.60, 1.15, 0.75, '2023-09-05', 20, 30, 20, 1.0, 3.0),
        ('Batata doce', 0.50, 1.15, 0.65, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Beterraba', 0.50, 1.05, 0.95, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Mandioca – ano 1', 0.30, 0.80, 0.30, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Mandioca – ano 2', 0.30, 1.10, 0.50, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Amendoim', 0.40, 1.15, 0.60, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Ervilha fresca', 0.50, 1.15, 1.10, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Ervilha seca', 0.50, 1.15, 0.30, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Feijão seco', 0.40, 1.15, 0.35, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Feijão verde', 0.50, 1.05, 0.90, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Lentilha', 0.40, 1.10, 0.30, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Soja', 0.50, 1.15, 0.50, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Alcachofra', 0.50, 1.00, 0.95, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Aspargo', 0.50, 0.95, 0.30, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Hortelã', 0.60, 1.15, 1.10, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Morango', 0.40, 0.85, 0.75, '2023-08-20', 25, 30, 30, 1.0, 3.0),
        ('Algodão', 0.35, 1.15, 0.50, '2023-10-01', 30, 50, 40, 1.0, 3.0),
        ('Linho', 0.35, 1.10, 0.25, '2023-10-01', 30, 50, 40, 1.0, 3.0),
        ('Sisal com estresse', 0.35, 0.40, 0.40, '2023-10-01', 30, 50, 40, 1.0, 3.0),
        ('Sisal sem estresse', 0.35, 0.70, 0.70, '2023-10-01', 30, 50, 40, 1.0, 3.0),
        ('Canola', 0.35, 1.15, 0.35, '2023-10-01', 30, 50, 40, 1.0, 3.0),
        ('Gergelim', 0.35, 1.10, 0.25, '2023-10-01', 30, 50, 40, 1.0, 3.0),
        ('Girassol', 0.35, 1.15, 0.35, '2023-10-01', 30, 50, 40, 1.0, 3.0),
        ('Mamona', 0.35, 1.15, 0.55, '2023-10-01', 30, 50, 40, 1.0, 3.0),
        ('Arroz', 1.05, 1.20, 0.90, '2023-07-01', 20, 35, 30, 1.0, 3.0),
        ('Aveia', 0.30, 1.15, 0.25, '2023-07-01', 20, 35, 30, 1.0, 3.0),
        ('Cevada', 0.30, 1.15, 0.25, '2023-07-01', 20, 35, 30, 1.0, 3.0),
        ('Milho doce', 0.30, 1.15, 1.05, '2023-07-01', 20, 35, 30, 1.0, 3.0),
        ('Painço', 0.30, 1.00, 0.30, '2023-07-01', 20, 35, 30, 1.0, 3.0),
        ('Sorgo-grão', 0.30, 1.00, 0.55, '2023-07-01', 20, 35, 30, 1.0, 3.0),
        ('Trigo (Primavera)', 0.30, 1.15, 0.25, '2023-07-01', 20, 35, 30, 1.0, 3.0)
    ]

    for cultura in culturas:
        cursor.execute('''
            INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce)
            SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM culturas WHERE nome = ?)
        ''', cultura + (cultura[0],))

    conn.commit()
    conn.close()

def get_culturas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce FROM culturas ORDER BY nome')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_bancos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, taxa_mensal FROM bancos ORDER BY id')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_banco(nome, taxa_mensal):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bancos (nome, taxa_mensal)
        VALUES (?, ?)
    ''', (nome, taxa_mensal))
    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return row_id

def delete_banco(banco_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bancos WHERE id = ?', (banco_id,))
    conn.commit()
    conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO projetos_metadados (
                codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario,
                nome_projetista, codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dados.get('codigo_projeto'),
            dados.get('nome_projeto'),
            dados.get('nome_propriedade'),
            dados.get('nome_proprietario'),
            dados.get('nome_projetista'),
            dados.get('codigo_subunidade'),
            dados.get('area_total_irrigada'),
            dados.get('area_subunidade'),
            dados.get('data_elaboracao')
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def insert_leitura(umidade, temperatura_max, temperatura_min, eto_calculada=0.0, cad_calculada=0.0, irn_calculada=0.0, comprimento_lateral_m=0.0, perda_carga_total_mca=0.0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO historico_leitura (umidade, temperatura_max, temperatura_min, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (umidade, temperatura_max, temperatura_min, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca))
    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return row_id

def get_ultima_leitura():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM historico_leitura
        ORDER BY id DESC LIMIT 1
    ''')
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def update_leitura_status(leitura_id, status_solo, tempo_irrigacao_calculado, eto_calculada=0.0, cad_calculada=0.0, irn_calculada=0.0, comprimento_lateral_m=0.0, perda_carga_total_mca=0.0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE historico_leitura
        SET status_solo = ?, tempo_irrigacao_calculado = ?, eto_calculada = ?, cad_calculada = ?, irn_calculada = ?, comprimento_lateral_m = ?, perda_carga_total_mca = ?
        WHERE id = ?
    ''', (status_solo, tempo_irrigacao_calculado, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca, leitura_id))
    conn.commit()
    conn.close()

def get_historico():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM historico_leitura
        ORDER BY id DESC LIMIT 10
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]





def obter_projeto_por_codigo(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def obter_resumo_hidraulico(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM historico_leitura
        WHERE codigo_projeto = ?
        ORDER BY id DESC LIMIT 1
    ''', (codigo_projeto,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_projeto_metadados(codigo_projeto):
    return obter_projeto_por_codigo(codigo_projeto)

def insert_projeto(dados):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO projetos_metadados (
                codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario,
                nome_projetista, codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dados.get('codigo_projeto'),
            dados.get('nome_projeto'),
            dados.get('nome_propriedade'),
            dados.get('nome_proprietario'),
            dados.get('nome_projetista'),
            dados.get('codigo_subunidade'),
            dados.get('area_total_irrigada'),
            dados.get('area_subunidade'),
            dados.get('data_elaboracao')
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
