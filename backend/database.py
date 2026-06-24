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
            codigo_projeto TEXT,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
    ''')
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
        CREATE TABLE IF NOT EXISTS bancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            taxa_mensal REAL NOT NULL
        )
    ''')

    # Unified projetos_metadados schema incorporating all fields and the new audit fields for Ps
    cursor.execute('''
    """)
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
            data_elaboracao TEXT,
            identificacao TEXT,
            nome_codigo_subunidade TEXT,
            largura INTEGER,
            altura INTEGER,
            profundidade INTEGER,
            tipo_calculo_ps TEXT CHECK(tipo_calculo_ps IN ('faixa_sombreada', 'diametro_copa', NULL)),
            ss_largura_faixa REAL,
            dco_diametro_copa REAL,
            ps_calculado REAL
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


            codigo_subunidade TEXT,
            area_total_irrigada REAL,
            area_subunidade REAL,
            data_elaboracao TEXT
        )
    ''')

    # Try to add missing columns in case the table already exists
    cursor.execute("PRAGMA table_info(projetos_metadados)")
    columns = [info[1] for info in cursor.fetchall()]
    novas_colunas = {
        'tipo_calculo_ps': 'TEXT CHECK(tipo_calculo_ps IN (\'faixa_sombreada\', \'diametro_copa\', NULL))',
        'ss_largura_faixa': 'REAL',
        'dco_diametro_copa': 'REAL',
        'ps_calculado': 'REAL'
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
def insert_projeto(codigo_projeto, nome_projeto, nome_propriedade, nome_proprietario, nome_projetista, identificacao, nome_codigo_subunidade, area_total_irrigada, area_subunidade, data_elaboracao):
def insert_projeto_metadados(codigo_projeto, nome_projeto, largura, altura, profundidade):
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
        return {"status": "sucesso", "id": row_id}
    except sqlite3.IntegrityError:
        return {"status": "erro", "mensagem": "Já existe um projeto com este código. O código do projeto deve ser único."}
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
    cursor.execute('SELECT COUNT(*) FROM culturas')
    count = cursor.fetchone()[0]
    if count == 0:
        culturas = [

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


    cursor.execute('SELECT COUNT(*) FROM culturas')
    count = cursor.fetchone()[0]

    if count == 0:
        for cultura in culturas:
            cursor.execute('''
                INSERT INTO culturas (nome, kc_inicial, kc_media, kc_final, data_plantio, dias_fase_inicial, dias_meia_estacao, dias_fase_final, min_ce, max_ce)
                SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT 1 FROM culturas WHERE nome = ?)
            ''', cultura + (cultura[0],))

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
    if count == 0:
        culturas = [
            ('Algodoeiro', 0.35, 1.20, 0.60, '2023-10-01', 30, 50, 40, 7.7, 27.0),
            ('Milho', 0.30, 1.20, 0.35, '2023-07-01', 20, 35, 30, 1.7, 10.0),
            ('Tomate', 0.60, 1.20, 0.90, '2023-09-01', 30, 40, 30, 2.5, 12.5),
            ('Alface', 0.70, 1.00, 0.95, '2023-09-15', 20, 30, 15, 1.3, 4.0),
            ('Cebola', 0.70, 1.05, 0.75, '2023-08-10', 15, 25, 20, 1.2, 7.2),
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
        cursor.executemany('''
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
def delete_banco(banco_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bancos WHERE id = ?', (banco_id,))
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

def insert_leitura(umidade, temperatura_max, temperatura_min, eto_calculada=0.0, cad_calculada=0.0, irn_calculada=0.0, comprimento_lateral_m=0.0, perda_carga_total_mca=0.0):
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





def salvar_dados_area_sombreada(codigo_projeto, tipo_calculo, ss_largura, dco_diametro, ps_calculado):
    conn = get_db_connection()
    cursor = conn.cursor()

    # First, check if the project exists
    cursor.execute('SELECT 1 FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False

    try:
        cursor.execute('''
            UPDATE projetos_metadados
            SET tipo_calculo_ps = ?,
                ss_largura_faixa = ?,
                dco_diametro_copa = ?,
                ps_calculado = ?
            WHERE codigo_projeto = ?
        ''', (tipo_calculo, ss_largura, dco_diametro, ps_calculado, codigo_projeto))
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

def insert_projeto_hidraulica_lateral(codigo_projeto, k_linha, se_vazao, q_media, lmax_perfil_ii_c, perfil_pressao_tipo):
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
        return False
    finally:
        conn.close()

def get_projeto_hidraulica_lateral(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projeto_hidraulica_lateral WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
