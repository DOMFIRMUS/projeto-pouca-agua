# -*- coding: utf-8 -*-
import math

class CalculadorIrrigacao:
    def calcular_cad(self, theta_cc, theta_pmp, z):
        if float(theta_cc) < float(theta_pmp) or float(z) <= 0:
            return 0.0
        cad = 1000.0 * (float(theta_cc) - float(theta_pmp)) * float(z)
        return round(cad, 2)

    def calcular_irn_p58(self, cad, fator_f, pe=0.0, tipo_irrigacao='total'):
        if tipo_irrigacao == 'total':
            irn = float(cad) * float(fator_f)
        elif tipo_irrigacao == 'suplementar':
            irn = (float(cad) * float(fator_f)) - float(pe)
        else:
            irn = 0.0

        if irn < 0.0:
            irn = 0.0
        return round(irn, 2)
