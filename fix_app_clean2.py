with open('backend/app_cleaned.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False

for i, line in enumerate(lines):
    # Fix the missing comma first
    if '"irrigacao_total_necessaria_mm": calc["itn"]\n' in line:
        line = line.replace('"irrigacao_total_necessaria_mm": calc["itn"]', '"irrigacao_total_necessaria_mm": calc["itn"],')

    if "se = request.args.get('se'" in line and "raio_umedecido_info =" in lines[i+9]:
        skip = True

    if skip and "raio_umedecido_info = calculador.calcular_raio_umedecido(alpha, q, ko, se)" in line:
        skip = False
        continue

    # Skip all the duplicate hideously merged git conflicts in app.py
    if line.strip() == "@app.route('/api/perda_carga', methods=['POST'])":
        skip = True

    if skip and line.strip() == "@app.route('/api/hidraulica', methods=['POST'])":
        skip = False
        continue

    # The duplicate metricas_tese keys also cause syntax errors.
    if '"tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos' in line and 'fracao_lixiviacao' in lines[i+1]:
        skip = True
    if skip and line.strip() == "}":
        skip = False

    if not skip:
        new_lines.append(line)

with open('backend/app_cleaned.py', 'w') as f:
    f.writelines(new_lines)
