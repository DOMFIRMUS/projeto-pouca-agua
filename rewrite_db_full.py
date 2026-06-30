import os

db_content = """# -*- coding: utf-8 -*-
import sqlite3

def get_db_connection():
    conn = sqlite3.connect("pouca_agua.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_leitura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            umidade REAL NOT NULL,
            temperatura_max REAL NOT NULL,
            temperatura_min REAL NOT NULL,
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
            largura REAL,
            altura REAL,
            profundidade REAL,
            fator_deplecao_f REAL,
            precipitacao_efetiva_pe REAL,
            tipo_irrigacao TEXT,
            cad_calculada REAL,
            irn_calculada REAL,
            tipo_calculo_ps TEXT,
            ss_largura_faixa REAL,
            dco_diametro_copa REAL,
            ps_calculado REAL,
            espacamento_fileiras_sr REAL,
            espacamento_plantas_sp REAL,
            diametro_molhado_dw REAL,
            num_gotejadores_np INTEGER,
            pw_calculado REAL
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
        CREATE TABLE IF NOT EXISTS projeto_perdas_conexoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_projeto TEXT NOT NULL,
            v_d REAL,
            d_d REAL,
            a_p REAL,
            hfl_d REAL,
            hfl_l REAL,
            vilaca_limites_status TEXT,
            FOREIGN KEY (codigo_projeto) REFERENCES projetos_metadados(codigo_projeto)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projeto_sistema_irrigacao (
            codigo_projeto TEXT PRIMARY KEY,
            pressao_h REAL,
            h_var_fraction REAL,
            declividade_so REAL,
            k_linha REAL,
            l_estimado REAL,
            razo_ponto_minimo REAL,
            lmax_ii_a REAL,
            lmax_ii_b REAL,
            tipo_perfil TEXT,
            FOREIGN KEY (codigo_projeto) REFERENCES projetos_metadados(codigo_projeto)
        )
    ''')

    conn.commit()
    conn.close()

def get_ultima_leitura():
    conn = get_db_connection()
    leitura = conn.execute('SELECT * FROM historico_leitura ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()
    if leitura:
        return dict(leitura)
    return None

def get_historico():
    conn = get_db_connection()
    historico = conn.execute('SELECT * FROM historico_leitura ORDER BY id DESC LIMIT 20').fetchall()
    conn.close()
    return [dict(row) for row in historico]

def insert_leitura(umidade, temperatura_max, temperatura_min, status_solo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO historico_leitura (umidade, temperatura_max, temperatura_min, status_solo)
        VALUES (?, ?, ?, ?)
    ''', (umidade, temperatura_max, temperatura_min, status_solo))
    conn.commit()
    conn.close()

def update_leitura_status(id, tempo_irrigacao_calculado, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE historico_leitura
        SET tempo_irrigacao_calculado = ?,
            eto_calculada = ?,
            cad_calculada = ?,
            irn_calculada = ?,
            comprimento_lateral_m = ?,
            perda_carga_total_mca = ?
        WHERE id = ?
    ''', (tempo_irrigacao_calculado, eto_calculada, cad_calculada, irn_calculada, comprimento_lateral_m, perda_carga_total_mca, id))
    conn.commit()
    conn.close()

def seed_culturas():
    pass

def get_culturas():
    conn = get_db_connection()
    culturas = conn.execute('SELECT * FROM culturas').fetchall()
    conn.close()
    return [dict(row) for row in culturas]

def get_bancos():
    conn = get_db_connection()
    bancos = conn.execute('SELECT * FROM bancos').fetchall()
    conn.close()
    return [dict(row) for row in bancos]

def insert_banco(nome, taxa_mensal):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO bancos (nome, taxa_mensal) VALUES (?, ?)', (nome, taxa_mensal))
    conn.commit()
    conn.close()

def delete_banco(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bancos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def insert_projeto(codigo_projeto, nome_projeto, largura, altura, profundidade):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projetos_metadados (codigo_projeto, nome_projeto, largura, altura, profundidade)
            VALUES (?, ?, ?, ?, ?)
        ''', (codigo_projeto, nome_projeto, largura, altura, profundidade))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_projeto_metadados(codigo_projeto):
    conn = get_db_connection()
    projeto = conn.execute('SELECT * FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,)).fetchone()
    conn.close()
    if projeto:
        return dict(projeto)
    return None

def obter_projeto_por_codigo(codigo_projeto):
    return get_projeto_metadados(codigo_projeto)

def vincular_cultura_projeto(codigo_projeto, cultura_id):
    pass

def update_area_umedecida_projeto(codigo_projeto, pw_calculado, num_gotejadores_np, espacamento_fileiras_sr, espacamento_plantas_sp, diametro_molhado_dw):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE projetos_metadados
        SET pw_calculado = ?, num_gotejadores_np = ?, espacamento_fileiras_sr = ?, espacamento_plantas_sp = ?, diametro_molhado_dw = ?
        WHERE codigo_projeto = ?
    ''', (pw_calculado, num_gotejadores_np, espacamento_fileiras_sr, espacamento_plantas_sp, diametro_molhado_dw, codigo_projeto))
    conn.commit()
    conn.close()

def update_area_sombreada_projeto(codigo_projeto, ps_calculado, tipo_calculo_ps, ss_largura_faixa, dco_diametro_copa):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE projetos_metadados
        SET ps_calculado = ?, tipo_calculo_ps = ?, ss_largura_faixa = ?, dco_diametro_copa = ?
        WHERE codigo_projeto = ?
    ''', (ps_calculado, tipo_calculo_ps, ss_largura_faixa, dco_diametro_copa, codigo_projeto))
    conn.commit()
    conn.close()

def salvar_dados_solo_p58(codigo_projeto, fator_f, pe, tipo_irrigacao, cad, irn):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE projetos_metadados
        SET fator_deplecao_f = ?, precipitacao_efetiva_pe = ?, tipo_irrigacao = ?, cad_calculada = ?, irn_calculada = ?
        WHERE codigo_projeto = ?
    ''', (fator_f, pe, tipo_irrigacao, cad, irn, codigo_projeto))
    conn.commit()
    conn.close()

def salvar_projeto_hidraulica_lateral(codigo_projeto, pressao_h, h_var_fraction, declividade_so, k_linha, l_estimado, razo_ponto_minimo, lmax_ii_a, lmax_ii_b, tipo_perfil):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projeto_sistema_irrigacao (codigo_projeto, pressao_h, h_var_fraction, declividade_so, k_linha, l_estimado, razo_ponto_minimo, lmax_ii_a, lmax_ii_b, tipo_perfil)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(codigo_projeto) DO UPDATE SET
            pressao_h=excluded.pressao_h, h_var_fraction=excluded.h_var_fraction, declividade_so=excluded.declividade_so, k_linha=excluded.k_linha, l_estimado=excluded.l_estimado, razo_ponto_minimo=excluded.razo_ponto_minimo, lmax_ii_a=excluded.lmax_ii_a, lmax_ii_b=excluded.lmax_ii_b, tipo_perfil=excluded.tipo_perfil
        ''', (codigo_projeto, pressao_h, h_var_fraction, declividade_so, k_linha, l_estimado, razo_ponto_minimo, lmax_ii_a, lmax_ii_b, tipo_perfil))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def obter_resumo_hidraulico(codigo_projeto):
    return None
"""

with open("backend/database.py", "w") as f:
    f.write(db_content)

print("Rewritten backend/database.py fully.")
