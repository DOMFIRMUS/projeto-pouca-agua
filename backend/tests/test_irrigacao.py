import sys
import os

# Add the backend directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.irrigacao import CalculadorIrrigacao

def test_avaliar_status_solo_critico():
    calc = CalculadorIrrigacao()
    resultado = calc.avaliar_status_solo(30.0)
    assert resultado["status"] == "Crítico (Seco)"
    assert resultado["irrigar"] is True

def test_avaliar_status_solo_moderado():
    calc = CalculadorIrrigacao()
    resultado = calc.avaliar_status_solo(50.0)
    assert resultado["status"] == "Moderado"
    assert resultado["irrigar"] is True

def test_avaliar_status_solo_ideal():
    calc = CalculadorIrrigacao()
    resultado = calc.avaliar_status_solo(70.0)
    assert resultado["status"] == "Ideal"
    assert resultado["irrigar"] is False

def test_avaliar_status_solo_encharcado():
    calc = CalculadorIrrigacao()
    resultado = calc.avaliar_status_solo(90.0)
    assert resultado["status"] == "Encharcado"
    assert resultado["irrigar"] is False

def test_calcular_eto_blaney_criddle():
    calc = CalculadorIrrigacao()
    # t_media = 25, mes_index = 1
    # P for Jan is 25
    # ETo = (0.457 * 25 + 8.13) * (25 / 100) = (11.425 + 8.13) * 0.25 = 19.555 * 0.25 = 4.88875 -> 4.89
    eto = calc.calcular_eto_blaney_criddle(25, 1)
    assert eto == 4.89

def test_calcular_eto_hargreaves():
    calc = CalculadorIrrigacao()
    # ETo para Janeiro (mes_index = 1), Tmax=30, Tmin=20
    # Tmedia = 25. Ra = 42.2
    # ETo = 0.0023 * 42.2 * 0.408 * (25 + 17.8) * sqrt(10)
    eto = calc.calcular_eto_hargreaves(30, 20, -22, 1)
    assert isinstance(eto, float)
    assert eto > 0

def test_calcular_irn_e_cad():
    calc = CalculadorIrrigacao()
    # to_cc=0.3, to_pmp=0.15, z=0.4, f=0.5, fw_percent=100
    # cad = 1000 * (0.3 - 0.15) * 0.4 = 60
    # irn_max = 60 * 0.5 * 1.0 = 30
    cad, irn_max = calc.calcular_irn_e_cad(0.3, 0.15, 0.4, 0.5, 100)
    assert cad == 60.0
    assert irn_max == 30.0

def test_calcular_kl():
    calc = CalculadorIrrigacao()
    # Test Keller
    assert calc.calcular_kl('Keller', 0.5) == round(0.5 + 0.15 * (1 - 0.5), 2)
    # Test Bernardo
    assert calc.calcular_kl('Bernardo', 0.5) == 0.5
    # Test Fereres
    assert calc.calcular_kl('Fereres', 0.70) == 1.0
    assert calc.calcular_kl('Fereres', 0.50) == round((1.09 * 0.50) + 0.30, 2)
    assert calc.calcular_kl('Fereres', 0.15) == round((1.94 * 0.15) + 0.10, 2)
    # Test Keller_Bliesner
    assert calc.calcular_kl('Keller_Bliesner', 0.25) == round(0.10 * 5.0, 2)  # sqrt(25) = 5
    # Test Fallback
    assert calc.calcular_kl('Desconhecido', 0.5) == 1.0

def test_calcular_etc():
    calc = CalculadorIrrigacao()
    # etc = eto * kc * kl
    # 5.0 * 1.2 * 0.8 = 4.8
    assert calc.calcular_etc(5.0, 1.2, 0.8) == 4.8
    # Com KL padrão de 1.0
    # 4.0 * 1.1 * 1.0 = 4.4
    assert calc.calcular_etc(4.0, 1.1) == 4.4
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

def test_calcular_itn():
    calc = CalculadorIrrigacao()
    # irn_mm = 30, ce_agua_ds_m = 1.0, ce_solo_min = 1.0, ce_solo_max = 2.0, uniformidade_emissao_decimal = 0.90
    # FL = 1.0 / (2 * 2.0) = 0.25
    # ITN = 30 / ((1 - 0.25) * 1.0 * 0.90) = 30 / (0.75 * 0.9) = 30 / 0.675 = 44.444...
    fl, itn = calc.calcular_itn(30, 1.0, 1.0, 2.0, 0.90)
    assert fl == 0.25
    assert itn == 44.44
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

def test_calcular_turno_rega_max():
    calc = CalculadorIrrigacao()
    # irn_max_mm=13.0, etc_mm_dia=5.0, sp_m=0.5, sr_m=1.0
    # TR_max = floor(13.0 / (5.0 * 0.5 * 1.0)) = floor(13.0 / 2.5) = floor(5.2) = 5
    tr_max = calc.calcular_turno_rega_max(13.0, 5.0, 0.5, 1.0)
    assert tr_max == 5

    # Caso com valores zerados para etc_mm_dia, sp_m ou sr_m
    tr_max_zero = calc.calcular_turno_rega_max(13.0, 0, 0.5, 1.0)
    assert tr_max_zero == 0
def test_comprimento_trecho_a_trecho():
    calc = CalculadorIrrigacao()
    # Parâmetros de teste: diametro_m=0.016, vazao_emissor_m3s=5.5e-7 (aprox 2L/h)
    # espacamento_m=0.3, pressao_entrada=10, declividade=0, hvar_max=2
    comprimento = calc.comprimento_trecho_a_trecho(
        diametro_m=0.016,
        vazao_emissor_m3s=5.5e-7,
        espacamento_m=0.3,
        pressao_entrada_mca=10.0,
        declividade=0.0,
        hvar_max=2.0
    )
    assert isinstance(comprimento, float)
    assert comprimento > 0.0

def test_perda_conector_lateral():
    calc = CalculadorIrrigacao()
    # Valores de exemplo: diam=0.016, comp=0.05, vel_con=1.5, vel_lat=1.0
    # hfl_l = 2.268121 * (0.016 ** 0.106) * (0.05 ** 1.057) * (1.5 ** 1.766) * (1.0 ** 0.386)
    # 0.016**0.106 ~= 0.648
    # 0.05**1.057 ~= 0.0426
    # 1.5**1.766 ~= 2.046
    # 1.0**0.386 = 1.0
    # 2.268121 * 0.648 * 0.0426 * 2.046 ~= 0.126
    perda = calc.perda_conector_lateral(0.016, 0.05, 1.5, 1.0)
    assert isinstance(perda, float)
    assert round(perda, 3) == 0.126

def test_calcular_pressao_inicial_bomba():
    calc = CalculadorIrrigacao()
    # pressao_emissor = 10.0
    # perda_tubulacao = 2.0
    # hfl_l calculada acima = 0.126
    # pressao_inicial = 10.0 + 2.0 + 0.126 = 12.126
    pressao = calc.calcular_pressao_inicial_bomba(10.0, 2.0, 0.016, 0.05, 1.5, 1.0)
    assert isinstance(pressao, float)
    assert round(pressao, 3) == 12.126
