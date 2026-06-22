#!/bin/bash
sed -i 's/"vazao_emissor_qa": 2.0/"vazao_emissor_qa": 2.0,/' backend/app.py
sed -i 's/"espacamento_fileiras_m": 1.0   # Espaçamento entre fileiras/"espacamento_fileiras_m": 1.0,   # Espaçamento entre fileiras/' backend/app.py
sed -i 's/sr_m=dados_sistema\["espacamento_fileiras_m"\]/sr_m=dados_sistema\["espacamento_fileiras_m"\]\n    )/' backend/app.py
sed -i 's/"numero_emissores_por_planta": np_emissores/"numero_emissores_por_planta": np_emissores,/' backend/app.py
sed -i '/"tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos/d' backend/app.py
sed -i '/"tempo_irrigacao_calculado_minutos": max(tempo_estimado_minutos, 0.0)/d' backend/app.py
