with open('backend/database.py', 'r') as f:
    content = f.read()

func = """
def salvar_dados_area_umedecida(codigo_projeto, dados):
    \"\"\"
    Atualiza os dados de área umedecida para um projeto existente na tabela projetos_metadados.
    Retorna True se atualizou alguma linha, False caso contrário.
    \"\"\"
    conn = get_db_connection()
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()
    return rows_affected > 0
"""

if 'salvar_dados_area_umedecida' not in content:
    with open('backend/database.py', 'a') as f:
        f.write("\n" + func + "\n")
