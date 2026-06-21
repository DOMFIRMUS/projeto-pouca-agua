import sys

def patch_file():
    with open('backend/tests/test_irrigacao.py', 'r') as f:
        content = f.read()

    new_content = content.replace(
'''<<<<<<< HEAD
def test_classificar_perfil_pressao():
    calc = CalculadorIrrigacao()

    # Teste para So <= 0 -> Perfil Tipo I
    assert calc.classificar_perfil_pressao(-0.01, 1, 1) == 'Perfil Tipo I (Aclive ou Nível)'
    assert calc.classificar_perfil_pressao(0, 1, 1) == 'Perfil Tipo I (Aclive ou Nível)'

    # Para razao = So / J
    # Teste para 0 < razao < 1 -> Perfil Tipo IIa
    # J = 1 * (1**1.75) = 1
    # So = 0.5 -> razao = 0.5
    assert calc.classificar_perfil_pressao(0.5, 1, 1) == 'Perfil Tipo IIa (Declive Fraco)'

    # Teste para razao == 1 -> Perfil Tipo IIb
    # J = 1 * (1**1.75) = 1
    # So = 1.0 -> razao = 1.0
    assert calc.classificar_perfil_pressao(1.0, 1, 1) == 'Perfil Tipo IIb (Declive Moderado)'

    # Teste para 1 < razao < 2.75 -> Perfil Tipo IIc
    # J = 1 * (1**1.75) = 1
    # So = 2.0 -> razao = 2.0
    assert calc.classificar_perfil_pressao(2.0, 1, 1) == 'Perfil Tipo IIc (Declive Forte)'

    # Teste para razao >= 2.75 -> Perfil Tipo IId
    # J = 1 * (1**1.75) = 1
    # So = 3.0 -> razao = 3.0
    assert calc.classificar_perfil_pressao(3.0, 1, 1) == 'Perfil Tipo IId (Declive Muito Forte)'
    assert calc.classificar_perfil_pressao(2.75, 1, 1) == 'Perfil Tipo IId (Declive Muito Forte)'
=======
def test_calcular_fator_obstrucao():
    calc = CalculadorIrrigacao()

    # Test 'online'
    # IO = 5 / 10 = 0.5
    # KL = 1.935 * (0.5 ** 0.595) = 1.2811
    kl_online = calc.calcular_fator_obstrucao('online', 10.0, 5.0)
    assert round(kl_online, 4) == 1.2811

    # Test 'pastilha'
    # IO = 5 / 10 = 0.5
    # KL = 1.383 * (0.5 ** 0.576) = 0.9277
    kl_pastilha = calc.calcular_fator_obstrucao('pastilha', 10.0, 5.0)
    assert round(kl_pastilha, 4) == 0.9277

    # Test 'bobi'
    # IO = 5 / 10 = 0.5
    # KL = 1.230 * (0.5 ** 0.510) = 0.8637
    kl_bobi = calc.calcular_fator_obstrucao('bobi', 10.0, 5.0)
    assert round(kl_bobi, 4) == 0.8637

    # Test unknown
    kl_unknown = calc.calcular_fator_obstrucao('unknown', 10.0, 5.0)
    assert kl_unknown == 0.0

    # Test zero area_tubo
    kl_zero = calc.calcular_fator_obstrucao('online', 0.0, 5.0)
    assert kl_zero == 0.0

def test_calcular_perda_carga_total():
    calc = CalculadorIrrigacao()
    # f_tubo=0.02, L=100, D=0.016, V=1.5
    # tipo_emissor='online', area_tubo=200, area_emissor=20
    # IO = 0.1
    # kl_online = 1.935 * (0.1 ** 0.595) = 0.4917
    # hf = (0.02 + 0.4917) * (100 / 0.016) * (1.5 ** 2) / (2 * 9.81)
    # hf = 0.5117 * 6250 * 2.25 / 19.62 = 366.7576 (rounded differently above)

    hf = calc.calcular_perda_carga_total(0.02, 100, 0.016, 1.5, 'online', 200, 20)
    assert round(hf, 4) == 366.7575

    # Test D = 0
    hf_zero = calc.calcular_perda_carga_total(0.02, 100, 0.0, 1.5, 'online', 200, 20)
    assert hf_zero == 0.0
>>>>>>> origin/main''',
'''def test_classificar_perfil_pressao():
    calc = CalculadorIrrigacao()

    # Teste para So <= 0 -> Perfil Tipo I
    assert calc.classificar_perfil_pressao(-0.01, 1, 1) == 'Perfil Tipo I (Aclive ou Nível)'
    assert calc.classificar_perfil_pressao(0, 1, 1) == 'Perfil Tipo I (Aclive ou Nível)'

    # Para razao = So / J
    # Teste para 0 < razao < 1 -> Perfil Tipo IIa
    # J = 1 * (1**1.75) = 1
    # So = 0.5 -> razao = 0.5
    assert calc.classificar_perfil_pressao(0.5, 1, 1) == 'Perfil Tipo IIa (Declive Fraco)'

    # Teste para razao == 1 -> Perfil Tipo IIb
    # J = 1 * (1**1.75) = 1
    # So = 1.0 -> razao = 1.0
    assert calc.classificar_perfil_pressao(1.0, 1, 1) == 'Perfil Tipo IIb (Declive Moderado)'

    # Teste para 1 < razao < 2.75 -> Perfil Tipo IIc
    # J = 1 * (1**1.75) = 1
    # So = 2.0 -> razao = 2.0
    assert calc.classificar_perfil_pressao(2.0, 1, 1) == 'Perfil Tipo IIc (Declive Forte)'

    # Teste para razao >= 2.75 -> Perfil Tipo IId
    # J = 1 * (1**1.75) = 1
    # So = 3.0 -> razao = 3.0
    assert calc.classificar_perfil_pressao(3.0, 1, 1) == 'Perfil Tipo IId (Declive Muito Forte)'
    assert calc.classificar_perfil_pressao(2.75, 1, 1) == 'Perfil Tipo IId (Declive Muito Forte)'

def test_calcular_fator_obstrucao():
    calc = CalculadorIrrigacao()

    # Test 'online'
    # IO = 5 / 10 = 0.5
    # KL = 1.935 * (0.5 ** 0.595) = 1.2811
    kl_online = calc.calcular_fator_obstrucao('online', 10.0, 5.0)
    assert round(kl_online, 4) == 1.2811

    # Test 'pastilha'
    # IO = 5 / 10 = 0.5
    # KL = 1.383 * (0.5 ** 0.576) = 0.9277
    kl_pastilha = calc.calcular_fator_obstrucao('pastilha', 10.0, 5.0)
    assert round(kl_pastilha, 4) == 0.9277

    # Test 'bobi'
    # IO = 5 / 10 = 0.5
    # KL = 1.230 * (0.5 ** 0.510) = 0.8637
    kl_bobi = calc.calcular_fator_obstrucao('bobi', 10.0, 5.0)
    assert round(kl_bobi, 4) == 0.8637

    # Test unknown
    kl_unknown = calc.calcular_fator_obstrucao('unknown', 10.0, 5.0)
    assert kl_unknown == 0.0

    # Test zero area_tubo
    kl_zero = calc.calcular_fator_obstrucao('online', 0.0, 5.0)
    assert kl_zero == 0.0

def test_calcular_perda_carga_total():
    calc = CalculadorIrrigacao()
    # f_tubo=0.02, L=100, D=0.016, V=1.5
    # tipo_emissor='online', area_tubo=200, area_emissor=20
    # IO = 0.1
    # kl_online = 1.935 * (0.1 ** 0.595) = 0.4917
    # hf = (0.02 + 0.4917) * (100 / 0.016) * (1.5 ** 2) / (2 * 9.81)
    # hf = 0.5117 * 6250 * 2.25 / 19.62 = 366.7576 (rounded differently above)

    hf = calc.calcular_perda_carga_total(0.02, 100, 0.016, 1.5, 'online', 200, 20)
    assert round(hf, 4) == 366.7575

    # Test D = 0
    hf_zero = calc.calcular_perda_carga_total(0.02, 100, 0.0, 1.5, 'online', 200, 20)
    assert hf_zero == 0.0''')

    with open('backend/tests/test_irrigacao.py', 'w') as f:
        f.write(new_content)

patch_file()
