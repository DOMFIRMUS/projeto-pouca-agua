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
            dias_fase_final INTEGER,
            min_ce REAL,
            max_ce REAL
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
    cursor.execute('SELECT id, nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce FROM culturas ORDER BY nome')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

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
