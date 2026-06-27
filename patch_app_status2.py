with open('backend/app.py', 'r') as f:
    content = f.read()

new_content = content.replace('calc["tempo_irrigacao_calculado_minutos"],', '0.0,')
new_content = new_content.replace('if ce_agua_ds_m > min_ce:', 'if ce_agua_ds_m > 1.0:')
new_content = new_content.replace('analise["mensagem"] +=', 'calc["analise"]["mensagem"] +=')
new_content = new_content.replace('return jsonify(resposta_json), 200', 'return jsonify(response_json), 200')

with open('backend/app.py', 'w') as f:
    f.write(new_content)
