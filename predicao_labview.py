#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Python 3.6 para predição de potência - Integração LabVIEW
Uso: python3 predicao_labview.py <corrente_max> <corrente_min> <corrente_media>
"""

import sys
import joblib
import pandas as pd


def main():
    """Função principal para predição via LabVIEW."""

    # Verificar argumentos
    if len(sys.argv) != 4:
        print("ERRO: 3 argumentos necessários")
        sys.exit(1)

    try:
        # Ler argumentos da linha de comando
        corrente_max = float(sys.argv[1])
        corrente_min = float(sys.argv[2])
        corrente_media = float(sys.argv[3])

        # Carregar modelo com joblib
        modelo = joblib.load("modelo_svm_potencia.sav")

        # Calcular atributos derivados (necessários para o modelo)
        amplitude_corrente = corrente_max - corrente_min
        razao_max_media = corrente_max / (corrente_media + 1e-6)

        # Criar DataFrame com os 5 atributos na ordem correta
        entrada = pd.DataFrame(
            [
                [
                    corrente_max,
                    corrente_min,
                    corrente_media,
                    amplitude_corrente,
                    razao_max_media,
                ]
            ],
            columns=[
                "corrente_max_A",
                "corrente_min_A",
                "corrente_media_A",
                "amplitude_corrente",
                "razao_max_media",
            ],
        )

        # Fazer predição
        classe_predita = int(modelo.predict(entrada)[0])
        probabilidades = modelo.predict_proba(entrada)[0]

        prob_baixa = float(probabilidades[0])
        prob_alta = float(probabilidades[1])

        # Saída formatada para LabVIEW (separado por pipe |)
        # Formato: CLASSE|PROB_BAIXA|PROB_ALTA
        print("{}|{:.6f}|{:.6f}".format(classe_predita, prob_baixa, prob_alta))

        # Retornar código de sucesso
        sys.exit(0)

    except FileNotFoundError:
        print("ERRO: modelo_svm_potencia.sav não encontrado")
        sys.exit(1)

    except ValueError as e:
        print("ERRO: Valores inválidos - {}".format(e))
        sys.exit(1)

    except Exception as e:
        print("ERRO: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
