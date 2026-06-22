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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_leitura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            codigo_projeto TEXT,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
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
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projetos_metadados (
            codigo_projeto TEXT PRIMARY KEY UNIQUE,
            nome_projeto TEXT,
            nome_propriedade TEXT,
            nome_proprietario TEXT,
            nome_projetista TEXT,
            identificacao TEXT,
            nome_codigo_subunidade TEXT,
            area_total_irrigada REAL,
            area_subunidade REAL,
            data_elaboracao TEXT,
            cultura_id INTEGER,
            estagio_selecionado TEXT CHECK(estagio_selecionado IN ('inicial', 'meia_estacao', 'final')),
            tipo_disposicao TEXT,
            configuracao_linha TEXT,
            parametro_alpha REAL,
            condutividade_ko REAL,
            profundidade_z REAL,
            tipo_calculo TEXT,
            ss_largura_faixa REAL,
            dco_diametro_copa REAL,
            rw_raio_umedecido REAL,
            dw_diametro_molhado REAL,
            pw_area_umedecida REAL,
            ps_area_sombreada REAL,
            FOREIGN KEY (cultura_id) REFERENCES culturas (id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            taxa_mensal REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def vincular_cultura_projeto(codigo_projeto, cultura_id, estagio_selecionado):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projetos_metadados
        SET cultura_id = ?, estagio_selecionado = ?
        WHERE codigo_projeto = ?
    """, (cultura_id, estagio_selecionado, codigo_projeto))
    conn.commit()
    conn.close()

def update_area_umedecida_projeto(codigo_projeto, rw, dw, pw, tipo_disposicao, configuracao_linha, parametro_alpha, condutividade_ko, profundidade_z):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projetos_metadados
        SET rw_raio_umedecido = ?, dw_diametro_molhado = ?, pw_area_umedecida = ?,
            tipo_disposicao = ?, configuracao_linha = ?, parametro_alpha = ?, condutividade_ko = ?, profundidade_z = ?
        WHERE codigo_projeto = ?
    """, (rw, dw, pw, tipo_disposicao, configuracao_linha, parametro_alpha, condutividade_ko, profundidade_z, codigo_projeto))
    conn.commit()
    conn.close()

def update_area_sombreada_projeto(codigo_projeto, ps, tipo_calculo, ss_largura_faixa, dco_diametro_copa):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projetos_metadados
        SET ps_area_sombreada = ?, tipo_calculo = ?, ss_largura_faixa = ?, dco_diametro_copa = ?
        WHERE codigo_projeto = ?
    """, (ps, tipo_calculo, ss_largura_faixa, dco_diametro_copa, codigo_projeto))
    conn.commit()
    conn.close()


def insert_projeto(codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario, nome_projetista, identificacao, nome_codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO projetos_metadados (
                codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario,
                nome_projetista, identificacao, nome_codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            codigo_projeto,
            nome_projeto,
            nome_propriedade,
            nome_proprietario,
            nome_projetista,
            identificacao,
            nome_codigo_subunidade,
            area_total_irrigada,
            area_subunidade,
            data_elaboracao
        ))
        row_id = cursor.lastrowid
        conn.commit()
        return {"status": "sucesso", "id": row_id}
    except sqlite3.IntegrityError:
        return {"status": "erro", "mensagem": "Já existe um projeto com este código. O código do projeto deve ser único."}
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
    cursor.execute('SELECT COUNT(*) FROM culturas')
    count = cursor.fetchone()[0]
    if count == 0:
        culturas = [
            ('Tomate tutorado', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 1.0, 3.0),
            ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15, 1.0, 3.0),
            ('Batata', 0.50, 1.15, 0.75, '2023-08-20', 25, 30, 30, 1.0, 3.0),
            ('Cebola seca', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.0, 3.0),
            ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30, 1.0, 3.0),
            ('Melancia', 0.40, 1.00, 0.75, '2023-09-05', 20, 30, 20, 1.0, 3.0)
        ]
        cursor.executemany("""
            INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, culturas)
        conn.commit()
    conn.close()

def get_culturas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce FROM culturas ORDER BY nome')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_cultura(nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce=1.0, max_ce=3.0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce))
    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return row_id

def insert_leitura(umidade, temperatura_max, temperatura_min, eto_calculada=0.0, cad_calculada=0.0, irn_calculada=0.0, comprimento_lateral_m=0.0, perda_carga_total_mca=0.0, codigo_projeto=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historico_leitura (umidade, temperatura_max, temperatura_min, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca, codigo_projeto)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (umidade, temperatura_max, temperatura_min, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca, codigo_projeto))
    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return row_id

def get_ultima_leitura():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM historico_leitura ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def update_leitura_status(leitura_id, status_solo, tempo_irrigacao_calculado, eto_calculada=0.0, cad_calculada=0.0, irn_calculada=0.0, comprimento_lateral_m=0.0, perda_carga_total_mca=0.0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE historico_leitura
        SET status_solo = ?, tempo_irrigacao_calculado = ?, eto_calculada = ?, cad_calculada = ?, irn_calculada = ?, comprimento_lateral_m = ?, perda_carga_total_mca = ?
        WHERE id = ?
    """, (status_solo, tempo_irrigacao_calculado, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca, leitura_id))
    conn.commit()
    conn.close()

def get_historico(codigo_projeto=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if codigo_projeto:
        cursor.execute("SELECT * FROM historico_leitura WHERE codigo_projeto = ? ORDER BY data_hora DESC LIMIT 10", (codigo_projeto,))
    else:
        cursor.execute("SELECT * FROM historico_leitura ORDER BY data_hora DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
