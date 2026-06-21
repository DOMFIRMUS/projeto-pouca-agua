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

def test_corrigir_fator_deplecao():
    calc = CalculadorIrrigacao()
    # f_tabela = 0.5, etc = 3.0 -> f = 0.5 + 0.04 * (5 - 3) = 0.5 + 0.08 = 0.58
    assert calc.corrigir_fator_deplecao(0.5, 3.0) == 0.58
    # Testar limite superior: f_tabela = 0.8, etc = 1.0 -> f = 0.8 + 0.04 * 4 = 0.96 -> max(0.8)
    assert calc.corrigir_fator_deplecao(0.8, 1.0) == 0.8
    # Testar limite inferior: f_tabela = 0.2, etc = 8.0 -> f = 0.2 + 0.04 * -3 = 0.08 -> min(0.1)
    assert calc.corrigir_fator_deplecao(0.2, 8.0) == 0.1

def test_calcular_irn_e_cad():
    calc = CalculadorIrrigacao()
    # to_cc=0.3, to_pmp=0.15, z=0.4, f=0.5, fw_percent=100
    # cad = 1000 * (0.3 - 0.15) * 0.4 = 60
    # Sem etc_calculada: irn_max = 60 * 0.5 * 1.0 = 30
    cad, irn_max = calc.calcular_irn_e_cad(0.3, 0.15, 0.4, 0.5, 100)
    assert cad == 60.0
    assert irn_max == 30.0

def test_calcular_perda_carga():
    calc = CalculadorIrrigacao()
    # Test valid input
    resultado = calc.calcular_perda_carga(16, 2, 0.5, 50)
    assert resultado["vazao_total_lh"] == 200.0
    assert "perda_carga_mca" in resultado
    assert resultado["status"] in ["Aceitável", "Desuniformidade Elevada"]

    # Test invalid input (espacamento <= 0)
    resultado_erro1 = calc.calcular_perda_carga(16, 2, 0, 50)
    assert "erro" in resultado_erro1

    # Test invalid input (diametro <= 0)
    resultado_erro2 = calc.calcular_perda_carga(0, 2, 0.5, 50)
    assert "erro" in resultado_erro2
    # Com etc_calculada = 3.0: f_corrigido = 0.58
    # irn_max = 60 * 0.58 * 1.0 = 34.8
    cad_corr, irn_max_corr = calc.calcular_irn_e_cad(0.3, 0.15, 0.4, 0.5, 100, etc_calculada=3.0)
    assert cad_corr == 60.0
    assert irn_max_corr == 34.8

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

def test_obter_kc_atual():
    calc = CalculadorIrrigacao()
    import datetime

    # Mock parameters
    data_plantio = datetime.date.today() - datetime.timedelta(days=25)
    dias_fases = {'inicial': 20, 'meia_estacao': 30, 'final': 20}
    kc_valores = {'inicial': 0.5, 'media': 1.0, 'final': 0.8}

    # Test age = 25, which is >= 20 and <= 20+30 (50) -> should be media
    kc = calc.obter_kc_atual(data_plantio, dias_fases, kc_valores)
    assert kc == 1.0

    # Test age = 10 (inicial)
    data_plantio_ini = datetime.date.today() - datetime.timedelta(days=10)
    kc_ini = calc.obter_kc_atual(data_plantio_ini, dias_fases, kc_valores)
    assert kc_ini == 0.5

    # Test age = 60 (final)
    data_plantio_fin = datetime.date.today() - datetime.timedelta(days=60)
    kc_fin = calc.obter_kc_atual(data_plantio_fin, dias_fases, kc_valores)
    assert kc_fin == 0.8
def test_calcular_tempo_irrigacao():
    calc = CalculadorIrrigacao()
    ti, np = calc.calcular_tempo_irrigacao(10.0, 0.5, 1.0, 50.0, 0.3, 2.0)
    assert np == 4
    assert ti == 0.625
def test_dimensionar_diametro_trecho():
    calc = CalculadorIrrigacao()
    # f=0.02, q=0.005, dz=2.0, L=100.0, h0=10.0
    # hf = 2.0
    # D = ((8.263e-2 * 0.02 * (0.005**2) * 100.0) / 2.0) ** 0.2
    # D = ((0.0016526 * 0.000025 * 100.0) / 2.0) ** 0.2
    # D = ((0.0000041315) / 2.0) ** 0.2 = (0.00000206575) ** 0.2
    # D ~ 0.072948
    d_teorico = calc.dimensionar_diametro_trecho(0.02, 0.005, 2.0, 100.0, 10.0)
    assert round(d_teorico, 6) == 0.072948

    # Test dz <= 0
    d_zero = calc.dimensionar_diametro_trecho(0.02, 0.005, 0.0, 100.0, 10.0)
    assert d_zero == 0.0
def test_fracionar_tempo_irrigacao():
    calc = CalculadorIrrigacao()
    # Test with typical value
    resultado1 = calc.fracionar_tempo_irrigacao(3.5, 2.0)
    assert resultado1['tempo_total_horas'] == 3.5
    assert resultado1['numero_ciclos'] == 2
    assert resultado1['horas_por_ciclo'] == 1.75
    assert resultado1['tempo_descanso_recomendado_horas'] == 1.0

    # Test exact boundary
    resultado2 = calc.fracionar_tempo_irrigacao(2.0, 2.0)
    assert resultado2['tempo_total_horas'] == 2.0
    assert resultado2['numero_ciclos'] == 1
    assert resultado2['horas_por_ciclo'] == 2.0

    # Test zero
    resultado3 = calc.fracionar_tempo_irrigacao(0.0)
    assert resultado3['tempo_total_horas'] == 0.0
    assert resultado3['numero_ciclos'] == 0
def test_calcular_area_umedecida():
    calc = CalculadorIrrigacao()
    # Test values:
    # q_vazao = 2.0 (L/h)
    # volume_z = 30.0 (L)
    # ko_condutividade = 15.0 (mm/h)
    # espacamento_plantas_sp = 2.0 (m)
    # espacamento_fileiras_sr = 3.0 (m)
    # numero_emissores_np = 1

    # Dw = 1.32 * ((30.0 * 2.0) / 15.0) ** (1/3)
    # Dw = 1.32 * (60.0 / 15.0) ** (1/3)
    # Dw = 1.32 * 4.0 ** (1/3)
    # 4.0 ** (1/3) is approximately 1.5874
    # Dw = 1.32 * 1.5874 = 2.0953 -> rounded 2.10

    # Pw = 1 * ((math.pi * (2.0953 ** 2)) / (4 * 2.0 * 3.0)) * 100
    # math.pi * 4.390 / 24.0 * 100
    # 3.14159 * 4.390 / 24.0 * 100 = 13.791 / 24.0 * 100 = 57.46% -> rounded

    dw, pw = calc.calcular_area_umedecida(2.0, 30.0, 15.0, 2.0, 3.0, 1)

    assert dw == 2.10
    # Recalculate accurate expectation based on precision
    import math
    dw_calc = 1.32 * ((30.0 * 2.0) / 15.0) ** (1/3)
    pw_calc = 1 * ((math.pi * (dw_calc ** 2)) / (4 * 2.0 * 3.0)) * 100
    assert pw == round(pw_calc, 2)

    # Test division by zero handlers
    dw_zero, pw_zero = calc.calcular_area_umedecida(2.0, 30.0, 0.0, 2.0, 3.0, 1)
    assert dw_zero == 0.0
    assert pw_zero == 0.0
def test_perda_direta_derivacao():
    calc = CalculadorIrrigacao()
    # Test with vd = 1.0, dd = 0.016, ap = 0.0001
    # Hfl_d = 0.043695 * (1.0 ** 1.897) * (0.016 ** -2.428) * (0.0001 ** 1.109)
    # Hfl_d = 0.043695 * 1.0 * 23157.079 * 0.0000363078
    # Hfl_d ~= 0.0367

    hfl_d = calc.perda_direta_derivacao(1.0, 0.016, 0.0001)

    # We can calculate the exact expected mathematical result inline to be robust
    expected = round(0.043695 * (1.0 ** 1.897) * (0.016 ** -2.428) * (0.0001 ** 1.109), 4)
    assert hfl_d == expected

    # Test dd = 0
    hfl_d_zero = calc.perda_direta_derivacao(1.0, 0.0, 0.0001)
    assert hfl_d_zero == 0.0
def test_calcular_area_sombreada():
    calc = CalculadorIrrigacao()

    # Test faixa continua
    # Ps = (largura_faixa_ss / espacamento_fileiras_sr) * 100
    # Ps = (1.5 / 3.0) * 100 = 50.0
    ps_faixa = calc.calcular_area_sombreada('faixa_continua', espacamento_plantas_sp=0.5, espacamento_fileiras_sr=3.0, largura_faixa_ss=1.5)
    assert ps_faixa == 50.0

    # Test arvore isolada
    # Ps = ((math.pi * (diametro_copa_dco ** 2) / 4) / (espacamento_fileiras_sr * espacamento_plantas_sp)) * 100
    # DCO = 2.0, SR = 4.0, SP = 3.0
    # Area copa = pi * 4 / 4 = pi = 3.14159...
    # Area plantio = 12.0
    # Ps = (3.14159... / 12) * 100 = 26.1799... -> 26.18
    import math
    ps_arvore = calc.calcular_area_sombreada('arvore_isolada', espacamento_plantas_sp=3.0, espacamento_fileiras_sr=4.0, diametro_copa_dco=2.0)
    assert ps_arvore == 26.18

    # Test edge case: invalid tipo
    ps_invalid = calc.calcular_area_sombreada('unknown', 1.0, 1.0)
    assert ps_invalid == 0.0

    # Test edge case: zero espacamento_fileiras_sr
    ps_zero_sr = calc.calcular_area_sombreada('faixa_continua', espacamento_plantas_sp=1.0, espacamento_fileiras_sr=0.0, largura_faixa_ss=1.0)
    assert ps_zero_sr == 0.0

    # Test edge case: missing largura_faixa_ss for faixa_continua
    ps_missing_ss = calc.calcular_area_sombreada('faixa_continua', espacamento_plantas_sp=1.0, espacamento_fileiras_sr=1.0)
    assert ps_missing_ss == 0.0

    # Test edge case: missing diametro_copa_dco for arvore_isolada
    ps_missing_dco = calc.calcular_area_sombreada('arvore_isolada', espacamento_plantas_sp=1.0, espacamento_fileiras_sr=1.0)
    assert ps_missing_dco == 0.0

    # Test edge case: zero espacamento_plantas_sp for arvore_isolada
    ps_zero_sp = calc.calcular_area_sombreada('arvore_isolada', espacamento_plantas_sp=0.0, espacamento_fileiras_sr=1.0, diametro_copa_dco=1.0)
    assert ps_zero_sp == 0.0
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

def test_calcular_rns():
    calc = CalculadorIrrigacao()
    rso, rns = calc.calcular_rns(rs=20.0, ra=35.0, altitude_m=1000.0)

    # Rso = [0.75 + 2 * (1000 / 100000)] * 35.0
    # Rso = [0.75 + 0.02] * 35.0 = 0.77 * 35.0 = 26.95
    assert rso == 26.95

    # Rns = 0.77 * 20.0 = 15.40
    assert rns == 15.40
