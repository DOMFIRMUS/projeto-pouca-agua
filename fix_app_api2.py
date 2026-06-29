with open("backend/app.py", "r") as f:
    content = f.read()

content = content.replace(
    "rn, g, t_media, u2, es_calculado, ea_calculado, delta, gama",
    "rn, g, t_media, u2, es_calculado, ea_calculado, delta, gama = 0, 0, 0, 0, 0, 0, 0, 0"
)

content = content.replace(
    "rn, g, t_media, u2, es, ea, delta, gama",
    "rn, g, t_media, u2, es, ea, delta, gama = 0, 0, 0, 0, 0, 0, 0, 0"
)

with open("backend/app.py", "w") as f:
    f.write(content)
