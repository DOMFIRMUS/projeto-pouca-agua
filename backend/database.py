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
        CREATE TABLE IF NOT EXISTS bancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            taxa_mensal REAL NOT NULL
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
            data_elaboracao TEXT,
            identificacao TEXT,
            nome_codigo_subunidade TEXT,
            largura INTEGER,
            altura INTEGER,
            profundidade INTEGER,
            tipo_calculo_ps TEXT CHECK(tipo_calculo_ps IN ('faixa_sombreada', 'diametro_copa', NULL)),
            ss_largura_faixa REAL,
            dco_diametro_copa REAL,
            ps_calculado REAL,
            cultura_id INTEGER,
            estagio_selecionado TEXT CHECK(estagio_selecionado IN ('inicial', 'meia_estacao', 'final')),
            tipo_disposicao TEXT,
            configuracao_linha TEXT,
            parametro_alpha REAL,
            condutividade_ko REAL,
            profundidade_z REAL,
            tipo_calculo TEXT,
            rw_raio_umedecido REAL,
            dw_diametro_molhado REAL,
            pw_area_umedecida REAL,
            ps_area_sombreada REAL,
            FOREIGN KEY (cultura_id) REFERENCES culturas (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projeto_derivacao_trechos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT,
            numero_trecho INTEGER,
            vazao_trecho REAL,
            comprimento_trecho REAL,
            delta_z REAL,
            diametro_teorico REAL,
            diametro_comercial REAL,
            hf_calculado REAL,
            pressao_final REAL,
            FOREIGN KEY(codigo_projeto) REFERENCES projetos_metadados(codigo_projeto)
        )
    ''')

    conn.commit()
    conn.close()

def inserir_trechos_derivacao(codigo_projeto, trechos_db_formatados):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM projeto_derivacao_trechos WHERE codigo_projeto = ?", (codigo_projeto,))
        query = '''
            INSERT INTO projeto_derivacao_trechos
            (codigo_projeto, numero_trecho, vazao_trecho, comprimento_trecho, delta_z, diametro_teorico, diametro_comercial, hf_calculado, pressao_final)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        cursor.executemany(query, trechos_db_formatados)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def vincular_cultura_projeto(codigo_projeto, cultura_id, estagio_selecionado):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE projetos_metadados
        SET cultura_id = ?, estagio_selecionado = ?
        WHERE codigo_projeto = ?
    ''', (cultura_id, estagio_selecionado, codigo_projeto))
    conn.commit()
    conn.close()

def update_area_umedecida_projeto(codigo_projeto, rw, dw, pw, tipo_disposicao, configuracao_linha, parametro_alpha, condutividade_ko, profundidade_z):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE projetos_metadados
        SET rw_raio_umedecido = ?, dw_diametro_molhado = ?, pw_area_umedecida = ?,
            tipo_disposicao = ?, configuracao_linha = ?, parametro_alpha = ?, condutividade_ko = ?, profundidade_z = ?
        WHERE codigo_projeto = ?
    ''', (rw, dw, pw, tipo_disposicao, configuracao_linha, parametro_alpha, condutividade_ko, profundidade_z, codigo_projeto))
    conn.commit()
    conn.close()

def update_area_sombreada_projeto(codigo_projeto, ps, tipo_calculo, ss_largura_faixa, dco_diametro_copa):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE projetos_metadados
        SET ps_area_sombreada = ?, tipo_calculo = ?, ss_largura_faixa = ?, dco_diametro_copa = ?
        WHERE codigo_projeto = ?
    ''', (ps, tipo_calculo, ss_largura_faixa, dco_diametro_copa, codigo_projeto))
    conn.commit()
    conn.close()

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

def get_projeto_metadados(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def obter_projeto_por_codigo(codigo_projeto):
    return get_projeto_metadados(codigo_projeto)

def obter_resumo_hidraulico(codigo_projeto):
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
            ('Tomate', 0.60, 1.15, 0.80, '2023-09-01', 30, 40, 30, 1.5, 3.0),
            ('Alface', 0.70, 1.00, 0.95, '2023-09-10', 20, 30, 15, 1.0, 2.5),
            ('Cenoura', 0.70, 1.05, 0.95, '2023-09-15', 20, 40, 30, 1.2, 2.8),
            ('Cebola', 0.70, 1.05, 0.75, '2023-08-20', 15, 35, 40, 1.0, 2.0),
            ('Melancia', 0.40, 1.00, 0.75, '2023-09-05', 20, 30, 20, 1.0, 3.0)
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
    cursor.execute('SELECT * FROM culturas ORDER BY nome')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_historico():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historico_leitura ORDER BY data_hora DESC LIMIT 100')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_ultima_leitura():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historico_leitura ORDER BY data_hora DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def update_leitura_status(id_leitura, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE historico_leitura SET status_solo = ? WHERE id = ?', (status, id_leitura))
    conn.commit()
    conn.close()

def insert_leitura(codigo_projeto, umidade, temperatura_max, temperatura_min, status_solo, tempo_irrigacao_calculado, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO historico_leitura (
            codigo_projeto, umidade, temperatura_max, temperatura_min, status_solo,
            tempo_irrigacao_calculado, eto_calculada, cad_calculada, irn_calculada,
            comprimento_lateral_m, perda_carga_total_mca
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (codigo_projeto, umidade, temperatura_max, temperatura_min, status_solo, tempo_irrigacao_calculado, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca))
    conn.commit()
    conn.close()

def get_bancos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bancos ORDER BY nome')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_banco(nome, taxa_mensal):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO bancos (nome, taxa_mensal) VALUES (?, ?)', (nome, taxa_mensal))
    conn.commit()
    conn.close()

def delete_banco(banco_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bancos WHERE id = ?', (banco_id,))
    conn.commit()
    conn.close()

def salvar_dados_area_sombreada(codigo_projeto, nome_projeto, largura, altura, profundidade, tipo_calculo_ps, ss_largura_faixa, dco_diametro_copa, ps_calculado):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE projetos_metadados
        SET tipo_calculo_ps = ?, ss_largura_faixa = ?, dco_diametro_copa = ?, ps_calculado = ?
        WHERE codigo_projeto = ?
    ''', (tipo_calculo_ps, ss_largura_faixa, dco_diametro_copa, ps_calculado, codigo_projeto))
    conn.commit()
    conn.close()
