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
            umidade REAL,
            temperatura_max REAL,
            temperatura_min REAL,
            status_solo TEXT,
            tempo_irrigacao_calculado REAL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
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
            dias_fase_final INTEGER
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
            ('Tomate tutorado', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30),
            ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15),
            ('Batata', 0.50, 1.15, 0.75, '2023-08-20', 25, 30, 30),
            ('Cebola seca', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20),
            ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30),
            ('Melancia', 0.40, 1.00, 0.75, '2023-09-05', 20, 30, 20)
        ]
        cursor.executemany('''
            INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', culturas)
        conn.commit()

    conn.close()

def get_culturas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final FROM culturas ORDER BY nome')
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

def insert_leitura(umidade, temperatura_max, temperatura_min):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO historico_leitura (umidade, temperatura_max, temperatura_min)
        VALUES (?, ?, ?)
    ''', (umidade, temperatura_max, temperatura_min))
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

def update_leitura_status(leitura_id, status_solo, tempo_irrigacao_calculado):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE historico_leitura
        SET status_solo = ?, tempo_irrigacao_calculado = ?
        WHERE id = ?
    ''', (status_solo, tempo_irrigacao_calculado, leitura_id))
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
