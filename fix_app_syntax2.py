with open('backend/app_fixed.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False

for i, line in enumerate(lines):
    if line.strip() == "@app.route('/api/hidraulica', methods=['POST'])" and lines[i+1].strip() == "def processar_hidraulica():" and lines[i+2].strip() == "":
        skip = True

    if skip and line.strip() == "@app.route('/api/hidraulica', methods=['POST'])":
        skip = False

    if not skip:
        new_lines.append(line)

with open('backend/app.py', 'w') as f:
    f.writelines(new_lines)
