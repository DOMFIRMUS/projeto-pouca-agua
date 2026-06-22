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
    conn.commit()
    conn.close()

def seed_culturas():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM culturas')
    count = cursor.fetchone()[0]

    culturas = [
        ('Melancia', 0.40, 1.00, 0.75, '2023-09-01', 20, 50, 20),
        ('Melão', 0.50, 1.05, 0.75, '2023-09-01', 25, 60, 20),
        ('Pepino', 0.60, 1.15, 0.75, '2023-09-01', 20, 50, 15),
        ('Batata', 0.50, 1.15, 0.75, '2023-09-01', 25, 65, 30),
        ('Batata doce', 0.50, 1.15, 0.65, '2023-09-01', 20, 65, 35),
        ('Beterraba', 0.50, 1.05, 0.95, '2023-09-01', 20, 50, 30),
        ('Mandioca - ano 1', 0.30, 0.80, 0.30, '2023-09-01', 20, 90, 30),
        ('Mandioca - ano 2', 0.30, 1.10, 0.50, '2023-09-01', 20, 120, 40),
        ('Amendoim', 0.40, 1.15, 0.60, '2023-09-01', 25, 75, 30),
        ('Ervilha fresca', 0.50, 1.15, 1.10, '2023-09-01', 20, 55, 15),
        ('Ervilha seca', 0.50, 1.15, 0.30, '2023-09-01', 20, 55, 25),
        ('Feijão seco', 0.40, 1.15, 0.35, '2023-09-01', 15, 65, 25),
        ('Feijão verde', 0.50, 1.05, 0.90, '2023-09-01', 15, 45, 15),
        ('Lentilha', 0.40, 1.10, 0.30, '2023-09-01', 20, 60, 20),
        ('Soja', 0.50, 1.15, 0.50, '2023-09-01', 20, 70, 25),
        ('Alcachofra', 0.50, 1.00, 0.95, '2023-09-01', 30, 100, 20),
        ('Aspargo', 0.50, 0.95, 0.30, '2023-09-01', 30, 120, 30),
        ('Hortelã', 0.60, 1.15, 1.10, '2023-09-01', 20, 60, 15),
        ('Morango', 0.40, 0.85, 0.75, '2023-09-01', 20, 60, 20),
        ('Algodão', 0.35, 1.15, 0.50, '2023-09-01', 30, 90, 30),
        ('Linho', 0.35, 1.10, 0.25, '2023-09-01', 25, 70, 25),
        ('Milho', 0.30, 1.20, 0.35, '2023-09-01', 20, 65, 30),
        ('Trigo (Primavera)', 0.30, 1.15, 0.25, '2023-09-01', 20, 60, 30),
        ('Sisal', 0.40, 1.05, 0.75, '2023-09-01', 30, 90, 30),
        ('Canola', 0.35, 1.15, 0.35, '2023-09-01', 20, 60, 20),
        ('Gergelim', 0.35, 1.10, 0.25, '2023-09-01', 20, 60, 20),
        ('Girassol', 0.35, 1.15, 0.35, '2023-09-01', 25, 70, 25),
        ('Mamona', 0.35, 1.15, 0.55, '2023-09-01', 30, 80, 30),
        ('Arroz', 1.05, 1.20, 0.90, '2023-09-01', 30, 60, 30),
        ('Aveia', 0.30, 1.15, 0.25, '2023-09-01', 20, 60, 25),
        ('Cevada', 0.30, 1.15, 0.25, '2023-09-01', 20, 60, 25),
        ('Milho doce', 0.30, 1.15, 1.05, '2023-09-01', 20, 50, 20),
        ('Painço', 0.30, 1.00, 0.30, '2023-09-01', 15, 50, 15),
        ('Sorgo-grão', 0.30, 1.10, 0.55, '2023-09-01', 20, 60, 20),
        ('Cenoura', 0.70, 1.05, 0.95, '2023-09-01', 20, 60, 20),
        ('Repolho', 0.70, 1.05, 0.95, '2023-09-01', 20, 60, 20),
        ('Aipo', 0.70, 1.05, 0.95, '2023-09-01', 20, 60, 20),
        ('Alho', 0.70, 1.00, 0.70, '2023-09-01', 20, 60, 20),
        ('Alface', 0.70, 1.00, 0.95, '2023-09-01', 20, 60, 20),
        ('Cebola seca', 0.70, 1.05, 0.75, '2023-09-01', 20, 60, 20),
        ('Cebolinha', 0.70, 1.00, 1.00, '2023-09-01', 20, 60, 20),
        ('Espinafre', 0.70, 1.00, 0.95, '2023-09-01', 20, 60, 20),
        ('Rabanete', 0.70, 0.90, 0.85, '2023-09-01', 20, 60, 20),
        ('Berinjela', 0.60, 1.05, 0.90, '2023-09-01', 20, 60, 20),
        ('Pimentão', 0.60, 1.05, 0.90, '2023-09-01', 20, 60, 20),
        ('Tomate', 0.60, 1.15, 0.80, '2023-09-01', 20, 60, 20),
        ('Abóbora', 0.50, 1.00, 0.80, '2023-09-01', 20, 60, 20),
        ('Abobrinha', 0.50, 0.95, 0.75, '2023-09-01', 20, 60, 20),
        ('Pastinaca', 0.50, 1.05, 0.95, '2023-09-01', 20, 60, 20),
        ('Nabo', 0.50, 1.10, 0.95, '2023-09-01', 20, 60, 20),
        ('Beterraba sacarina', 0.35, 1.20, 0.70, '2023-09-01', 20, 60, 20)
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final)
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
