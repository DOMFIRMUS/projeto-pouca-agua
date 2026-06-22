# -*- coding: utf-8 -*-
import sqlite3

def init_db():
    conn = sqlite3.connect("irrigacao.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projetos_metadados (
            codigo_projeto TEXT PRIMARY KEY,
            nome TEXT,
            cultura TEXT,
            profundidade_z REAL,
            fator_f REAL,
            precipitacao_efetiva REAL,
            tipo_irrigacao TEXT,
            cad_calculado REAL,
            irn_calculada REAL
        )
    """)
    conn.commit()
    conn.close()

def salvar_dados_solo_p58(codigo, f, pe, tipo, cad, irn):
    try:
        conn = sqlite3.connect("irrigacao.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE projetos_metadados
            SET fator_f = ?, precipitacao_efetiva = ?, tipo_irrigacao = ?, cad_calculado = ?, irn_calculada = ?
            WHERE codigo_projeto = ?
        """, (f, pe, tipo, cad, irn, codigo))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_db_connection():
    conn = sqlite3.connect("irrigacao.db")
    conn.row_factory = sqlite3.Row
    return conn
