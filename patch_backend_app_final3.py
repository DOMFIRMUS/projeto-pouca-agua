with open("backend/app.py", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if i == 439:
        new_lines.append(line.replace(",", "")) # remove trailing comma
        new_lines.append("        }\n")
        new_lines.append("    }\n")
        continue
    if i in [440, 441, 442]:
        continue # remove incorrectly placed lines
    new_lines.append(line)

with open("backend/app.py", "w") as f:
    f.writelines(new_lines)
