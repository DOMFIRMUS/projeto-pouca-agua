with open('backend/tests/test_app.py', 'r') as f:
    lines = f.readlines()

with open('backend/tests/test_app.py', 'w') as f:
    for i, line in enumerate(lines):
        if 137 <= i <= 170:
            continue
        f.write(line)
