import re

with open('backend/database.py', 'r') as f:
    content = f.read()

column_code = """
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
"""

if 'tipo_disposicao' not in content:
    new_content = content.replace("conn.commit()\n    conn.close()\n\n    if count == 0:\n", column_code + "\n    conn.close()\n")
    with open('backend/database.py', 'w') as f:
        f.write(new_content)
