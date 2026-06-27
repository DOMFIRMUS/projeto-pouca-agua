# -*- coding: utf-8 -*-
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
    conn = sqlite3.connect("irrigacao.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_leitura (

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projeto_perdas_conexoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT NOT NULL,
            v_d REAL,
            d_d REAL,
            a_p REAL,
            hfl_d REAL,
            d_c REAL,
            l_c REAL,
            v_c REAL,
            v_l REAL,
            hfl_l REAL,
            vilaca_limites_status INTEGER CHECK(vilaca_limites_status IN (0, 1)),
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (codigo_projeto) REFERENCES projetos_metadados(codigo_projeto)
        )
    ''')
cursor.execute('''
        CREATE TABLE IF NOT EXISTS projetos_metadados (
            codigo_projeto TEXT PRIMARY KEY,
            nome TEXT,
            cultura TEXT,
                CREATE TABLE IF NOT EXISTS historico_leitura (

    cursor.execute("""
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
            umidade REAL,
            temperatura_max REAL,
            temperatura_min REAL,
            status_solo TEXT,
            tempo_irrigacao_calculado REAL,
            eto_calculada REAL,
            cad_calculada REAL,
            irn_calculada REAL,
            comprimento_lateral_m REAL,
            perda_carga_total_mca REAL
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
            perda_carga_total_mca REAL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    """)
    cursor.execute("""
    """)
    cursor.execute("PRAGMA table_info(historico_leitura)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'codigo_projeto' not in columns:
        cursor.execute('ALTER TABLE historico_leitura ADD COLUMN codigo_projeto TEXT')
    cursor.execute("PRAGMA table_info(historico_leitura)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'codigo_projeto' not in columns:
        cursor.execute('ALTER TABLE historico_leitura ADD COLUMN codigo_projeto TEXT')
    cursor.execute("""

    cursor.execute("""
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
            nome TEXT,
            kc_inicial REAL,
            kc_media REAL,
            kc_final REAL,
            data_plantio TEXT,
            dias_fase_inicial INTEGER,
            dias_meia_estacao INTEGER,
            dias_fase_final INTEGER,

            min_ce REAL DEFAULT 1.0,
            max_ce REAL DEFAULT 3.0,
            f_tab REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            taxa_mensal REAL NOT NULL
        )
    """)

    # Unified projetos_metadados schema incorporating all fields and the new audit fields for Ps
    cursor.execute("""
    """)

    cursor.execute('''
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projeto_hidraulica_lateral (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT UNIQUE,
            pressao_h REAL,
            h_var_fraction REAL,
            declividade_so REAL,
            k_linha REAL,
            l_estimado REAL,
            razo_ponto_minimo_ell_l REAL,
            lmax_perfil_ii_a REAL,
            lmax_perfil_ii_b REAL,
            perfil_pressao_tipo TEXT,
            FOREIGN KEY (codigo_projeto) REFERENCES projetos_metadados(codigo_projeto)
        )
    """)

    # Unified projetos_metadados schema incorporating all fields and the new audit fields for Ps
    cursor.execute("""
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
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projetos_metadados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT UNIQUE NOT NULL,
            nome_projeto TEXT,
            nome_propriedade TEXT,
            nome_proprietario TEXT,
            nome_projetista TEXT,
            data_elaboracao TEXT,
            nome_codigo_subunidade TEXT,
            largura INTEGER,
            altura INTEGER,
            profundidade INTEGER,
            tipo_calculo_ps TEXT CHECK(tipo_calculo_ps IN ('faixa_sombreada', 'diametro_copa', NULL)),
            ss_largura_faixa REAL,
            dco_diametro_copa REAL,
            ps_calculado REAL,
            ps_calculado REAL
            data_elaboracao TEXT,
            largura INTEGER,
            altura INTEGER,
            profundidade INTEGER
        )
    ''')

    cursor.execute('''
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
            cultura_id INTEGER,
            FOREIGN KEY (cultura_id) REFERENCES culturas (id)
            fator_f REAL,
            precipitacao_efetiva REAL,
            tipo_irrigacao TEXT,
            cad_calculado REAL,
            irn_calculada REAL
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

    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projetos_metadados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT UNIQUE NOT NULL,
            nome_projeto TEXT,
            largura INTEGER,
            altura INTEGER,
            profundidade INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projeto_microirrigacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT NOT NULL,
            configuracao_linha TEXT,
            tipo_disposicao TEXT,
            condutividade_ko REAL,
            parametro_alpha REAL,
            vazao_q REAL,
            f_ajustado REAL,
            irn_max_calculada REAL,
            FOREIGN KEY (codigo_projeto) REFERENCES projetos_metadados(codigo_projeto)
        )
    """)

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projeto_hidraulica_lateral (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT UNIQUE,
            k_linha REAL,
            se_vazao REAL,
            q_media REAL,
            lmax_perfil_ii_c REAL,
            perfil_pressao_tipo TEXT,
            data_calculo DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
        CREATE TABLE IF NOT EXISTS projeto_hidraulica_derivacao (
            codigo_projeto TEXT PRIMARY KEY,
            declividade_derivacao REAL,
            pressao_entrada_h REAL,
            comprimento_total_l REAL,
            vazao_ql REAL,
            espacamento_sl REAL,
            distancia_sl1 REAL,
            variacao_hvar REAL,
            estrategia_dimensionamento TEXT,
            zitterell_faixa_status INTEGER,
            FOREIGN KEY(codigo_projeto) REFERENCES projetos_metadados(codigo_projeto)
        )
    ''')

    cursor.execute("PRAGMA table_info(projetos_metadados)")
    columns = [info[1] for info in cursor.fetchall()]
    novas_colunas = {
        'tipo_disposicao': 'TEXT',
        'configuracao_linha': 'TEXT',
        'parametro_alpha': 'REAL',
        'condutividade_ko': 'REAL',
        'profundidade_z': 'REAL',
        'rw_calculado': 'REAL',
        'dw_calculado': 'REAL',
        'pw_final': 'REAL'
    }

    for col_name, col_type in novas_colunas.items():
        if col_name not in columns:
            cursor.execute(f'ALTER TABLE projetos_metadados ADD COLUMN {col_name} {col_type}')
    ''')

    conn.commit()
    conn.close()
    """)
    conn.commit()
    conn.close()

def salvar_dados_solo_p58(codigo, f, pe, tipo, cad, irn):
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

def insert_projeto(codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario, nome_projetista, identificacao, nome_codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao):
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
    """, (ps, tipo_calculo, ss_largura_faixa, dco_diametro_copa, codigo_projeto))
    conn.commit()
    conn.close()




    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            taxa_mensal REAL NOT NULL
        )
    ''')

    # Try to add missing columns in case the table already exists
    cursor.execute("PRAGMA table_info(projetos_metadados)")
    columns = [info[1] for info in cursor.fetchall()]
    novas_colunas = {
        'tipo_calculo_ps': 'TEXT CHECK(tipo_calculo_ps IN (\'faixa_sombreada\', \'diametro_copa\', NULL))',
        'ss_largura_faixa': 'REAL',
        'dco_diametro_copa': 'REAL',
        'ps_calculado': 'REAL',
        'theta_cc': 'REAL',
        'theta_pmp': 'REAL',
        'fator_f': 'REAL',
        'cad_calculado': 'REAL',
        'irn_final': 'REAL',
        'turno_rega_final': 'INTEGER',
        'etc_calculado': 'REAL'
    }
    for col, tipo in novas_colunas.items():
        if col not in columns:
            try:
                cursor.execute(f'ALTER TABLE projetos_metadados ADD COLUMN {col} {tipo}')
            except Exception as e:
                pass

    conn.commit()

    conn.close()

def insert_projeto(dados):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
def insert_projeto_metadados(codigo_projeto, nome_projeto, largura, altura, profundidade):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        conn = sqlite3.connect("irrigacao.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO projetos_metadados (codigo_projeto, nome_projeto, largura, altura, profundidade)
            VALUES (?, ?, ?, ?, ?)
        """, (codigo_projeto, nome_projeto, largura, altura, profundidade))
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
    except Exception:
        cursor.execute("""
            INSERT INTO projetos_metadados (
                codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario,
                nome_projetista, codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
def insert_projeto_metadados(codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario, nome_projetista, identificacao, nome_codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
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

def seed_culturas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM culturas')
    count = cursor.fetchone()[0]
    if count == 0:
        pass

    culturas = [
        ('Algodoeiro', 0.35, 1.20, 0.60, '2023-10-01', 30, 50, 40, 7.7, 27.0, 0.65),
        ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30, 1.7, 10.0, 0.5),
        ('Tomate', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 2.5, 12.5, 0.4),
        ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15, 1.3, 4.0, 0.3),
        ('Cebola', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.2, 7.2, 0.5),
        ('Tomate tutorado', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 1.0, 3.0, 0.4),
        ('Batata', 0.50, 1.15, 0.75, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
        ('Cebola seca', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.0, 3.0, 0.5),
        ('Melancia', 0.40, 1.00, 0.75, '2023-09-05', 20, 30, 20, 1.0, 3.0, 0.4),
        ('Melão', 0.50, 1.05, 0.75, '2023-09-05', 20, 30, 20, 1.0, 3.0, 0.5),
        ('Pepino', 0.60, 1.15, 0.75, '2023-09-05', 20, 30, 20, 1.0, 3.0, 0.5),
        ('Batata doce', 0.50, 1.15, 0.65, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
        ('Beterraba', 0.50, 1.05, 0.95, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
        ('Mandioca – ano 1', 0.30, 0.80, 0.30, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
        ('Mandioca – ano 2', 0.30, 1.10, 0.50, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
        ('Amendoim', 0.40, 1.15, 0.60, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
        ('Ervilha fresca', 0.50, 1.15, 1.10, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
        ('Ervilha seca', 0.50, 1.15, 0.30, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
        ('Feijão seco', 0.40, 1.15, 0.35, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
        ('Feijão verde', 0.50, 1.05, 0.90, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
        ('Lentilha', 0.40, 1.10, 0.30, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
        ('Soja', 0.50, 1.15, 0.50, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5, 0.5),
        ('Alcachofra', 0.50, 1.00, 0.95, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5, 0.5),
        ('Aspargo', 0.50, 0.95, 0.30, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5, 0.5),
        ('Hortelã', 0.60, 1.15, 1.10, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5, 0.5),
        ('Morango', 0.40, 0.85, 0.75, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5, 0.5),
        ('Algodão', 0.35, 1.15, 0.50, '2023-10-01', 30, 50, 40, 1.0, 3.0, 0.65, 0.65),
        ('Linho', 0.35, 1.10, 0.25, '2023-10-01', 30, 50, 40, 1.0, 3.0, 0.5, 0.5),
        ('Sisal com estresse', 0.35, 0.40, 0.40, '2023-10-01', 30, 50, 40, 1.0, 3.0, 0.5, 0.5),
        ('Sisal sem estresse', 0.35, 0.70, 0.70, '2023-10-01', 30, 50, 40, 1.0, 3.0, 0.5, 0.5),
        ('Canola', 0.35, 1.15, 0.35, '2023-10-01', 30, 50, 40, 1.0, 3.0, 0.5, 0.5),
        ('Gergelim', 0.35, 1.10, 0.25, '2023-10-01', 30, 50, 40, 1.0, 3.0, 0.5, 0.5),
        ('Girassol', 0.35, 1.15, 0.35, '2023-10-01', 30, 50, 40, 1.0, 3.0, 0.5, 0.5),
        ('Mamona', 0.35, 1.15, 0.55, '2023-10-01', 30, 50, 40, 1.0, 3.0, 0.5, 0.5),
        ('Arroz', 1.05, 1.20, 0.90, '2023-07-01', 20, 35, 30, 1.0, 3.0, 0.5, 0.5),
        ('Aveia', 0.30, 1.15, 0.25, '2023-07-01', 20, 35, 30, 1.0, 3.0, 0.5, 0.5),
        ('Cevada', 0.30, 1.15, 0.25, '2023-07-01', 20, 35, 30, 1.0, 3.0, 0.5, 0.5),
        ('Milho doce', 0.30, 1.15, 1.05, '2023-07-01', 20, 35, 30, 1.0, 3.0, 0.5, 0.5),
        ('Painço', 0.30, 1.00, 0.30, '2023-07-01', 20, 35, 30, 1.0, 3.0, 0.5, 0.5),
        ('Sorgo-grão', 0.30, 1.00, 0.55, '2023-07-01', 20, 35, 30, 1.0, 3.0, 0.5, 0.5),
        ('Trigo (Primavera, 0.5)', 0.30, 1.15, 0.25, '2023-07-01', 20, 35, 30, 1.0, 3.0, 0.5)
    ]


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
            cursor.execute("""
                INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce)
                SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT 1 FROM culturas WHERE nome = ?)
            ''', cultura + (cultura[0],))
        conn.commit()
            """, cultura + (cultura[0],))

    culturas = [
        ('Melancia', 0.40, 1.00, 0.75, '2023-09-01', 20, 50, 20, 0.4, 0.4),
        ('Melão', 0.50, 1.05, 0.75, '2023-09-01', 25, 60, 20, 0.5, 0.5),
        ('Pepino', 0.60, 1.15, 0.75, '2023-09-01', 20, 50, 15, 0.5, 0.5),
        ('Batata', 0.50, 1.15, 0.75, '2023-09-01', 25, 65, 30, 0.5, 0.5),
        ('Batata doce', 0.50, 1.15, 0.65, '2023-09-01', 20, 65, 35, 0.5, 0.5),
        ('Beterraba', 0.50, 1.05, 0.95, '2023-09-01', 20, 50, 30, 0.5, 0.5),
        ('Mandioca - ano 1', 0.30, 0.80, 0.30, '2023-09-01', 20, 90, 30, 0.5, 0.5),
        ('Mandioca - ano 2', 0.30, 1.10, 0.50, '2023-09-01', 20, 120, 40, 0.5, 0.5),
        ('Amendoim', 0.40, 1.15, 0.60, '2023-09-01', 25, 75, 30, 0.5, 0.5),
        ('Ervilha fresca', 0.50, 1.15, 1.10, '2023-09-01', 20, 55, 15, 0.5, 0.5),
        ('Ervilha seca', 0.50, 1.15, 0.30, '2023-09-01', 20, 55, 25, 0.5, 0.5),
        ('Feijão seco', 0.40, 1.15, 0.35, '2023-09-01', 15, 65, 25, 0.5, 0.5),
        ('Feijão verde', 0.50, 1.05, 0.90, '2023-09-01', 15, 45, 15, 0.5, 0.5),
        ('Lentilha', 0.40, 1.10, 0.30, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Soja', 0.50, 1.15, 0.50, '2023-09-01', 20, 70, 25, 0.5, 0.5),
        ('Alcachofra', 0.50, 1.00, 0.95, '2023-09-01', 30, 100, 20, 0.5, 0.5),
        ('Aspargo', 0.50, 0.95, 0.30, '2023-09-01', 30, 120, 30, 0.5, 0.5),
        ('Hortelã', 0.60, 1.15, 1.10, '2023-09-01', 20, 60, 15, 0.5, 0.5),
        ('Morango', 0.40, 0.85, 0.75, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Algodão', 0.35, 1.15, 0.50, '2023-09-01', 30, 90, 30, 0.65, 0.65),
        ('Linho', 0.35, 1.10, 0.25, '2023-09-01', 25, 70, 25, 0.5, 0.5),
        ('Milho', 0.30, 1.20, 0.35, '2023-09-01', 20, 65, 30, 0.5, 0.5),
        ('Trigo (Primavera, 0.5)', 0.30, 1.15, 0.25, '2023-09-01', 20, 60, 30, 0.5, 0.5),
        ('Sisal', 0.40, 1.05, 0.75, '2023-09-01', 30, 90, 30, 0.5, 0.5),
        ('Canola', 0.35, 1.15, 0.35, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Gergelim', 0.35, 1.10, 0.25, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Girassol', 0.35, 1.15, 0.35, '2023-09-01', 25, 70, 25, 0.5, 0.5),
        ('Mamona', 0.35, 1.15, 0.55, '2023-09-01', 30, 80, 30, 0.5, 0.5),
        ('Arroz', 1.05, 1.20, 0.90, '2023-09-01', 30, 60, 30, 0.5, 0.5),
        ('Aveia', 0.30, 1.15, 0.25, '2023-09-01', 20, 60, 25, 0.5, 0.5),
        ('Cevada', 0.30, 1.15, 0.25, '2023-09-01', 20, 60, 25, 0.5, 0.5),
        ('Milho doce', 0.30, 1.15, 1.05, '2023-09-01', 20, 50, 20, 0.5, 0.5),
        ('Painço', 0.30, 1.00, 0.30, '2023-09-01', 15, 50, 15, 0.5, 0.5),
        ('Sorgo-grão', 0.30, 1.10, 0.55, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Cenoura', 0.70, 1.05, 0.95, '2023-09-01', 20, 60, 20, 0.35, 0.35),
        ('Repolho', 0.70, 1.05, 0.95, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Aipo', 0.70, 1.05, 0.95, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Alho', 0.70, 1.00, 0.70, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Alface', 0.70, 1.00, 0.95, '2023-09-01', 20, 60, 20, 0.3, 0.3),
        ('Cebola seca', 0.70, 1.05, 0.75, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Cebolinha', 0.70, 1.00, 1.00, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Espinafre', 0.70, 1.00, 0.95, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Rabanete', 0.70, 0.90, 0.85, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Berinjela', 0.60, 1.05, 0.90, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Pimentão', 0.60, 1.05, 0.90, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Tomate', 0.60, 1.15, 0.80, '2023-09-01', 20, 60, 20, 0.4, 0.4),
        ('Abóbora', 0.50, 1.00, 0.80, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Abobrinha', 0.50, 0.95, 0.75, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Pastinaca', 0.50, 1.05, 0.95, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Nabo', 0.50, 1.10, 0.95, '2023-09-01', 20, 60, 20, 0.5, 0.5),
        ('Beterraba sacarina', 0.35, 1.20, 0.70, '2023-09-01', 20, 60, 20, 0.5)
    ]
    for c in culturas:
        if len(c) == 9:
            pass
        elif len(c) == 10:
            c = c[:9]
        elif len(c) >= 11:
            c = c[:9]
        cursor.execute("""
            INSERT OR IGNORE INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, f_tab)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, c)
    cursor.executemany("""
        INSERT OR IGNORE INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1.0, 3.0)
    """, culturas)
    conn.commit()
    for cultura in culturas:
        cursor.execute("""
        INSERT OR IGNORE INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, culturas)
    conn.commit()
    if count == 0:
#        culturas = [
#            ('Algodoeiro', 0.35, 1.20, 0.60, '2023-10-01', 30, 50, 40, 7.7, 27.0),
#            ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30, 1.7, 10.0),
#            ('Tomate', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 2.5, 12.5),
#            ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15, 1.3, 4.0),
#            ('Cebola', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.2, 7.2),
#            ('Tomate tutorado', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 1.0, 3.0),
#            ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15, 1.0, 3.0),
#            ('Batata', 0.50, 1.15, 0.75, '2023-08-20', 25, 30, 30, 1.0, 3.0),
#            ('Cebola seca', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.0, 3.0),
#            ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30, 1.0, 3.0),
#            ('Melancia', 0.40, 1.00, 0.75, '2023-09-05', 20, 30, 20, 1.0, 3.0)
#        ]
#        cursor.executemany("""
#            INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce)
#            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#        """, culturas)
        culturas = [
            ('Algodoeiro', 0.35, 1.20, 0.60, '2023-10-01', 30, 50, 40, 7.7, 27.0, 0.65),
            ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30, 1.7, 10.0, 0.5),
            ('Tomate', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 2.5, 12.5, 0.4),
            ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15, 1.3, 4.0, 0.3),
            ('Cebola', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.2, 7.2, 0.5),
            ('Tomate tutorado', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 1.0, 3.0, 0.4),
            ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15, 1.0, 3.0, 0.3),
            ('Batata', 0.50, 1.15, 0.75, '2023-08-20', 25, 30, 30, 1.0, 3.0, 0.5),
            ('Cebola seca', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.0, 3.0, 0.5),
            ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30, 1.0, 3.0, 0.5),
            ('Melancia', 0.40, 1.00, 0.75, '2023-09-05', 20, 30, 20, 1.0, 3.0, 0.4)
            ('Algodoeiro', 0.35, 1.20, 0.60, '2023-10-01', 30, 50, 40, 7.7, 27.0),
            ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30, 1.7, 10.0),
            ('Tomate', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 2.5, 12.5),
            ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15, 1.3, 4.0),
            ('Cebola', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.2, 7.2)
            ('Cebola', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.2, 7.2),
            ('Tomate tutorado', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 1.0, 3.0),
            ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15, 1.0, 3.0),
            ('Batata', 0.50, 1.15, 0.75, '2023-08-20', 25, 30, 30, 1.0, 3.0),
            ('Cebola seca', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.0, 3.0),
            ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30, 1.0, 3.0),
            ('Melancia', 0.40, 1.00, 0.75, '2023-09-05', 20, 30, 20, 1.0, 3.0)
        ]
        cursor.executemany("""
            INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce, f_tab)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, culturas)
        conn.commit()

    for cultura in culturas:
        cursor.execute("""
            INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final)
            SELECT ?, ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM culturas WHERE nome = ?)
        """, cultura + (cultura[0],))
            INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce)
            SELECT ?, ?, ?, ?, ?, ?, ?, ?, 1.0, 3.0
            WHERE NOT EXISTS (SELECT 1 FROM culturas WHERE nome = ?)
        """, cultura + (cultura[0],))


    cursor.execute("PRAGMA table_info(projetos_metadados)")
    columns = [info[1] for info in cursor.fetchall()]
    novas_colunas = {
        'tipo_disposicao': 'TEXT',
        'configuracao_linha': 'TEXT',
        'parametro_alpha': 'REAL',
        'condutividade_ko': 'REAL',
        'profundidade_z': 'REAL',
        'rw_calculado': 'REAL',
        'dw_calculado': 'REAL',
        'pw_final': 'REAL'
    }

    for col_name, col_type in novas_colunas.items():
        if col_name not in columns:
            cursor.execute(f'ALTER TABLE projetos_metadados ADD COLUMN {col_name} {col_type}')

    conn.commit()

    conn.close()

def get_culturas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce, f_tab FROM culturas ORDER BY nome')
    cursor.execute('SELECT * FROM culturas ORDER BY nome')
    cursor.execute('SELECT * FROM culturas ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_cultura(nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce=1.0, max_ce=3.0, f_tab=0.50):
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

def get_historico():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historico_leitura ORDER BY data_hora DESC LIMIT 100')
    rows = cursor.fetchall()
def insert_cultura(nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce=1.0, max_ce=3.0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bancos ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_banco(nome, taxa_mensal):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bancos (nome, taxa_mensal)
        VALUES (?, ?)
    """, (nome, taxa_mensal))
    cursor.execute('INSERT INTO bancos (nome, taxa_mensal) VALUES (?, ?)', (nome, taxa_mensal))
    cursor.execute("""
        INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce, f_tab)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce, f_tab))
    row_id = cursor.lastrowid

    cursor.execute("PRAGMA table_info(projetos_metadados)")
    columns = [info[1] for info in cursor.fetchall()]
    novas_colunas = {
        'tipo_disposicao': 'TEXT',
        'configuracao_linha': 'TEXT',
        'parametro_alpha': 'REAL',
        'condutividade_ko': 'REAL',
        'profundidade_z': 'REAL',
        'rw_calculado': 'REAL',
        'dw_calculado': 'REAL',
        'pw_final': 'REAL'
    }

    for col_name, col_type in novas_colunas.items():
        if col_name not in columns:
            cursor.execute(f'ALTER TABLE projetos_metadados ADD COLUMN {col_name} {col_type}')

    conn.commit()

    conn.close()
    return row_id

def delete_banco(banco_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bancos WHERE id = ?', (banco_id,))

    cursor.execute("PRAGMA table_info(projetos_metadados)")
    columns = [info[1] for info in cursor.fetchall()]
    novas_colunas = {
        'tipo_disposicao': 'TEXT',
        'configuracao_linha': 'TEXT',
        'parametro_alpha': 'REAL',
        'condutividade_ko': 'REAL',
        'profundidade_z': 'REAL',
        'rw_calculado': 'REAL',
        'dw_calculado': 'REAL',
        'pw_final': 'REAL'
    }

    for col_name, col_type in novas_colunas.items():
        if col_name not in columns:
            cursor.execute(f'ALTER TABLE projetos_metadados ADD COLUMN {col_name} {col_type}')

    conn.commit()

    conn.close()
    return row_id

def delete_banco(banco_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bancos WHERE id = ?', (banco_id,))
    conn.commit()
    conn.close()



def insert_leitura(umidade, temperatura_max, temperatura_min, eto_calculada=0.0, cad_calculada=0.0, irn_calculada=0.0, comprimento_lateral_m=0.0, perda_carga_total_mca=0.0, codigo_projeto=None):
def insert_projeto(codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario, nome_projetista, identificacao, nome_codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao):
def insert_projeto(dados):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO projetos_metadados (
                codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario,
                nome_projetista, codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
def insert_leitura(umidade, temperatura_max, temperatura_min, eto_calculada=0.0, cad_calculada=0.0, irn_calculada=0.0, comprimento_lateral_m=0.0, perda_carga_total_mca=0.0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historico_leitura (umidade, temperatura_max, temperatura_min, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (umidade, temperatura_max, temperatura_min, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca))
        INSERT INTO historico_leitura (umidade, temperatura_max, temperatura_min, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca, codigo_projeto)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (umidade, temperatura_max, temperatura_min, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca, codigo_projeto))
    row_id = cursor.lastrowid

    cursor.execute("PRAGMA table_info(projetos_metadados)")
    columns = [info[1] for info in cursor.fetchall()]
    novas_colunas = {
        'tipo_disposicao': 'TEXT',
        'configuracao_linha': 'TEXT',
        'parametro_alpha': 'REAL',
        'condutividade_ko': 'REAL',
        'profundidade_z': 'REAL',
        'rw_calculado': 'REAL',
        'dw_calculado': 'REAL',
        'pw_final': 'REAL'
    }

    for col_name, col_type in novas_colunas.items():
        if col_name not in columns:
            cursor.execute(f'ALTER TABLE projetos_metadados ADD COLUMN {col_name} {col_type}')

    conn.commit()

    conn.close()
    return [dict(row) for row in rows]

def get_projeto_metadados(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historico_leitura ORDER BY data_hora DESC LIMIT 1')
    cursor.execute("""
        SELECT * FROM historico_leitura
        ORDER BY id DESC LIMIT 1
    """)
    cursor.execute('SELECT * FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    cursor.execute("SELECT * FROM historico_leitura ORDER BY id DESC LIMIT 1")
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
def get_projeto(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()
    cursor.execute("""
        UPDATE historico_leitura
        SET status_solo = ?, tempo_irrigacao_calculado = ?, eto_calculada = ?, cad_calculada = ?, irn_calculada = ?, comprimento_lateral_m = ?, perda_carga_total_mca = ?
        WHERE id = ?
    """, (status_solo, tempo_irrigacao_calculado, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca, leitura_id))

    cursor.execute("PRAGMA table_info(projetos_metadados)")
    columns = [info[1] for info in cursor.fetchall()]
    novas_colunas = {
        'tipo_disposicao': 'TEXT',
        'configuracao_linha': 'TEXT',
        'parametro_alpha': 'REAL',
        'condutividade_ko': 'REAL',
        'profundidade_z': 'REAL',
        'rw_calculado': 'REAL',
        'dw_calculado': 'REAL',
        'pw_final': 'REAL'
    }

    for col_name, col_type in novas_colunas.items():
        if col_name not in columns:
            cursor.execute(f'ALTER TABLE projetos_metadados ADD COLUMN {col_name} {col_type}')

    conn.commit()

    conn.close()
    if row:
        return dict(row)
    return None

def get_bancos():
def get_projetos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM historico_leitura
        ORDER BY id DESC LIMIT 10
    """)
    cursor.execute("SELECT * FROM projetos_metadados")
def get_historico(codigo_projeto=None):
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



    try:
        cursor.execute("""
            UPDATE projetos_metadados
            SET tipo_calculo_ps = ?,
                ss_largura_faixa = ?,
                dco_diametro_copa = ?,
                ps_calculado = ?
            WHERE codigo_projeto = ?
        """, (tipo_calculo, ss_largura, dco_diametro, ps_calculado, codigo_projeto))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error in salvar_dados_area_sombreada: {e}")
        return False
    finally:
        conn.close()

def obter_projeto_por_codigo(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None




def salvar_dados_area_sombreada(codigo_projeto, tipo_calculo, ss_largura, dco_diametro, ps_calculado):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM historico_leitura
        WHERE codigo_projeto = ?
        ORDER BY id DESC LIMIT 1
    """, (codigo_projeto,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_projeto_metadados(codigo_projeto):
    return obter_projeto_por_codigo(codigo_projeto)



def insert_projeto_microirrigacao(codigo_projeto, configuracao_linha, tipo_disposicao, condutividade_ko, parametro_alpha, vazao_q, f_ajustado, irn_max_calculada):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO projeto_microirrigacao (codigo_projeto, configuracao_linha, tipo_disposicao, condutividade_ko, parametro_alpha, vazao_q, f_ajustado, irn_max_calculada) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (codigo_projeto, configuracao_linha, tipo_disposicao, condutividade_ko, parametro_alpha, vazao_q, f_ajustado, irn_max_calculada))
    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return row_id

def insert_projeto(dados):
    conn = get_db_connection()
    cursor = conn.cursor()
    # First, check if the project exists
    cursor.execute('SELECT 1 FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False

    try:
        cursor.execute("""
            UPDATE projetos_metadados
            SET fator_f = ?, precipitacao_efetiva = ?, tipo_irrigacao = ?, cad_calculado = ?, irn_calculada = ?
            WHERE codigo_projeto = ?
        """, (tipo_calculo, ss_largura, dco_diametro, ps_calculado, codigo_projeto))
        """, (f, pe, tipo, cad, irn, codigo))
        conn.commit()
        conn.close()



def salvar_dados_area_umedecida(codigo_projeto, dados):
    """
    Atualiza os dados de área umedecida para um projeto existente na tabela projetos_metadados.
    Retorna True se atualizou alguma linha, False caso contrário.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM historico_leitura
        WHERE codigo_projeto = ?
        ORDER BY id DESC LIMIT 1
    """, (codigo_projeto,))
    row = cursor.fetchone()
    cursor.execute('''
        UPDATE projetos_metadados
        SET tipo_disposicao = ?,
            configuracao_linha = ?,
            parametro_alpha = ?,
            condutividade_ko = ?,
            profundidade_z = ?,
            rw_calculado = ?,
            dw_calculado = ?,
            pw_final = ?
        WHERE codigo_projeto = ?
    ''', (
        dados.get('tipo_disposicao'),
        dados.get('configuracao_linha'),
        dados.get('parametro_alpha'),
        dados.get('condutividade_ko'),
        dados.get('profundidade_z'),
        dados.get('rw_calculado'),
        dados.get('dw_calculado'),
        dados.get('pw_final'),
        codigo_projeto
    ))
    rows_affected = cursor.rowcount

    cursor.execute("PRAGMA table_info(projetos_metadados)")
    columns = [info[1] for info in cursor.fetchall()]
    novas_colunas = {
        'tipo_disposicao': 'TEXT',
        'configuracao_linha': 'TEXT',
        'parametro_alpha': 'REAL',
        'condutividade_ko': 'REAL',
        'profundidade_z': 'REAL',
        'rw_calculado': 'REAL',
        'dw_calculado': 'REAL',
        'pw_final': 'REAL'
    }

    for col_name, col_type in novas_colunas.items():
        if col_name not in columns:
            cursor.execute(f'ALTER TABLE projetos_metadados ADD COLUMN {col_name} {col_type}')

    conn.commit()

    conn.close()
    return rows_affected > 0
    if row:
        return dict(row)
    return None


def salvar_projeto_hidraulica_lateral(codigo_projeto, pressao_h, h_var_fraction, declividade_so, k_linha, l_estimado, razo_ponto, lmax_iia, lmax_iib, perfil_tipo):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO projeto_hidraulica_lateral (codigo_projeto, pressao_h, h_var_fraction, declividade_so, k_linha, l_estimado, razo_ponto_minimo_ell_l, lmax_perfil_ii_a, lmax_perfil_ii_b, perfil_pressao_tipo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(codigo_projeto) DO UPDATE SET pressao_h=excluded.pressao_h, h_var_fraction=excluded.h_var_fraction, declividade_so=excluded.declividade_so, k_linha=excluded.k_linha, l_estimado=excluded.l_estimado, razo_ponto_minimo_ell_l=excluded.razo_ponto_minimo_ell_l, lmax_perfil_ii_a=excluded.lmax_perfil_ii_a, lmax_perfil_ii_b=excluded.lmax_perfil_ii_b, perfil_pressao_tipo=excluded.perfil_pressao_tipo", (codigo_projeto, pressao_h, h_var_fraction, declividade_so, k_linha, l_estimado, razo_ponto, lmax_iia, lmax_iib, perfil_tipo))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving: {e}")
        cursor.execute("""
            INSERT INTO projetos_metadados (
                codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario,
                nome_projetista, codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
    except Exception:
    except:
        return False
    finally:
        conn.close()

def get_bancos():
    return []

def insert_banco(nome, taxa):
    pass

def salvar_dados_solo_irn(codigo_projeto, theta_cc, theta_pmp, fator_f, cad_calculado, irn_final, turno_rega_final):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False

    try:
        cursor.execute("""
            UPDATE projetos_metadados
            SET theta_cc = ?,
                theta_pmp = ?,
                fator_f = ?,
                cad_calculado = ?,
                irn_final = ?,
                turno_rega_final = ?
            WHERE codigo_projeto = ?
        """, (theta_cc, theta_pmp, fator_f, cad_calculado, irn_final, turno_rega_final, codigo_projeto))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error in salvar_dados_solo_irn: {e}")
        return False
    finally:
        conn.close()

def salvar_hidraulica_derivacao(codigo_projeto, declividade_derivacao, pressao_entrada_h,
                               comprimento_total_l, vazao_ql, espacamento_sl, distancia_sl1,
                               variacao_hvar, estrategia_dimensionamento, zitterell_faixa_status):

def salvar_perdas_conexoes(codigo_projeto, v_d, d_d, a_p, hfl_d, d_c, l_c, v_c, v_l, hfl_l, limites_status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    if not cursor.fetchone():
        conn.close()
        return False

    try:
        cursor.execute('''
            INSERT INTO projeto_hidraulica_derivacao (
                codigo_projeto, declividade_derivacao, pressao_entrada_h, comprimento_total_l,
                vazao_ql, espacamento_sl, distancia_sl1, variacao_hvar, estrategia_dimensionamento,
                zitterell_faixa_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(codigo_projeto) DO UPDATE SET
                declividade_derivacao=excluded.declividade_derivacao,
                pressao_entrada_h=excluded.pressao_entrada_h,
                comprimento_total_l=excluded.comprimento_total_l,
                vazao_ql=excluded.vazao_ql,
                espacamento_sl=excluded.espacamento_sl,
                distancia_sl1=excluded.distancia_sl1,
                variacao_hvar=excluded.variacao_hvar,
                estrategia_dimensionamento=excluded.estrategia_dimensionamento,
                zitterell_faixa_status=excluded.zitterell_faixa_status
        ''', (
            codigo_projeto, declividade_derivacao, pressao_entrada_h, comprimento_total_l,
            vazao_ql, espacamento_sl, distancia_sl1, variacao_hvar, estrategia_dimensionamento,
            zitterell_faixa_status
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error in salvar_hidraulica_derivacao: {e}")
        return False
    finally:
        conn.close()

def insert_projeto_hidraulica_lateral(codigo_projeto, k_linha, se_vazao, q_media, lmax_perfil_ii_c, perfil_pressao_tipo):
            INSERT INTO projeto_perdas_conexoes
            (codigo_projeto, v_d, d_d, a_p, hfl_d, d_c, l_c, v_c, v_l, hfl_l, vilaca_limites_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (codigo_projeto, v_d, d_d, a_p, hfl_d, d_c, l_c, v_c, v_l, hfl_l, limites_status))
        conn.commit()
        return True
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()

def salvar_hidraulica_lateral(codigo_projeto, perfil_pressao, lmax, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO projeto_hidraulica_lateral (
                codigo_projeto, k_linha, se_vazao, q_media, lmax_perfil_ii_c, perfil_pressao_tipo
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(codigo_projeto) DO UPDATE SET
                k_linha=excluded.k_linha,
                se_vazao=excluded.se_vazao,
                q_media=excluded.q_media,
                lmax_perfil_ii_c=excluded.lmax_perfil_ii_c,
                perfil_pressao_tipo=excluded.perfil_pressao_tipo,
                data_calculo=CURRENT_TIMESTAMP
        ''', (codigo_projeto, k_linha, se_vazao, q_media, lmax_perfil_ii_c, perfil_pressao_tipo))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error in insert_projeto_hidraulica_lateral: {e}")
            INSERT INTO projeto_hidraulica_lateral (codigo_projeto, perfil_pressao_final, lmax_final_calculado, denominador_seguro_status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(codigo_projeto) DO UPDATE SET
                perfil_pressao_final = excluded.perfil_pressao_final,
                lmax_final_calculado = excluded.lmax_final_calculado,
                denominador_seguro_status = excluded.denominador_seguro_status
        ''', (codigo_projeto, perfil_pressao, lmax, status))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error in salvar_hidraulica_lateral: {e}")
        return False
    finally:
        conn.close()

def get_bancos():
    return []
def insert_banco(nome, taxa):
    pass
def delete_banco(id):
    pass
def get_projeto_hidraulica_lateral(codigo_projeto):
def obter_hidraulica_lateral(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projeto_hidraulica_lateral WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
def get_bancos(): return []
def insert_banco(*args, **kwargs): pass
def delete_banco(*args, **kwargs): pass

def get_db_connection():
    conn = sqlite3.connect("irrigacao.db")
    conn.row_factory = sqlite3.Row
    return conn
