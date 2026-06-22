import sqlite3
from flask import current_app
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'pouca_agua.db')
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'pouca_agua.db')
DB_PATH = DATABASE_PATH

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_leitura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT,
            umidade REAL NOT NULL DEFAULT 0.0,
            temperatura_max REAL NOT NULL,
            temperatura_min REAL NOT NULL,
            t_max REAL,
            t_min REAL,
            ur_media REAL,
            n_insolacao REAL,
            metodo_eto TEXT,
            status_solo TEXT NOT NULL DEFAULT 'Pendente',
            tempo_irrigacao_calculado REAL DEFAULT 0.0,
            eto_calculada REAL DEFAULT 0.0,
            cad_calculada REAL DEFAULT 0.0,
            irn_calculada REAL DEFAULT 0.0,
            comprimento_lateral_m REAL DEFAULT 0.0,
            perda_carga_total_mca REAL DEFAULT 0.0,
            data_leitura TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS culturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            kc_inicial REAL NOT NULL,
            kc_media REAL NOT NULL,
            kc_final REAL NOT NULL,
            data_plantio DATE NOT NULL,
            dias_fase_inicial INTEGER NOT NULL,
            dias_meia_estacao INTEGER NOT NULL,
            dias_fase_final INTEGER NOT NULL,
            min_ce REAL,
            max_ce REAL
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
            data_elaboracao TEXT,
            largura INTEGER,
            altura INTEGER,
            profundidade INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            taxa_mensal REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def seed_culturas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM culturas')
    count = cursor.fetchone()[0]

    if count == 0:
        culturas = [
            ('Algodoeiro', 0.35, 1.20, 0.60, '2023-10-01', 30, 50, 40, 7.7, 27.0),
            ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30, 1.7, 10.0),
            ('Tomate', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 2.5, 12.5),
            ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15, 1.3, 4.0),
            ('Cebola', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.2, 7.2)
        ]
        cursor.executemany('''
            INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', culturas)
        conn.commit()
    conn.close()

def get_culturas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM culturas ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_leitura(codigo_projeto, t_max, t_min, ur_media, n_insolacao, metodo_eto, eto_calculada, data_leitura):
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO historico_leitura (codigo_projeto, umidade, temperatura_max, temperatura_min, t_max, t_min, ur_media, n_insolacao, metodo_eto, eto_calculada, data_leitura, status_solo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pendente')
        ''', (codigo_projeto, ur_media, t_max, t_min, t_max, t_min, ur_media, n_insolacao, metodo_eto, eto_calculada, data_leitura))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error in insert_leitura: {e}")
        raise e
    finally:
        conn.close()

def get_ultima_leitura():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historico_leitura ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def update_leitura_status(leitura_id, status_solo, tempo_irrigacao, eto=0.0, cad=0.0, irn=0.0, comp_lat=0.0, perda_carga=0.0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE historico_leitura
        SET status_solo = ?, tempo_irrigacao_calculado = ?,
            eto_calculada = ?, cad_calculada = ?, irn_calculada = ?,
            comprimento_lateral_m = ?, perda_carga_total_mca = ?
        WHERE id = ?
    ''', (status_solo, tempo_irrigacao, eto, cad, irn, comp_lat, perda_carga, leitura_id))
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

def get_bancos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bancos ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_banco(nome, taxa_mensal):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO bancos (nome, taxa_mensal) VALUES (?, ?)', (nome, taxa_mensal))
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

def insert_projeto(codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario, nome_projetista, identificacao, nome_codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        import sqlite3
        cursor.execute('''
            INSERT INTO projetos_metadados (codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario, nome_projetista, identificacao, nome_codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario, nome_projetista, identificacao, nome_codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao))
        row_id = cursor.lastrowid
        conn.commit()
        return {"status": "sucesso", "id": row_id}
    except sqlite3.IntegrityError:
        return {"status": "erro", "mensagem": "Já existe um projeto com este código. O código do projeto deve ser único."}
    finally:
        conn.close()

def insert_projeto_metadados(codigo_projeto, nome_projeto, largura, altura, profundidade):
    import sqlite3
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

def get_projeto(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_projetos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projetos_metadados")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
