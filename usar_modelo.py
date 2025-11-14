#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para usar o modelo SVM de classificação de potência.
Compatível com Python 3.6+

Uso:
    python usar_modelo.py <corrente_max> <corrente_min> <corrente_media>

Exemplo:
    python usar_modelo.py 1.80 -0.03 0.67

Para integração com LabVIEW:
    - LabVIEW chama este script via System Exec.vi
    - Passa os 3 valores de corrente como argumentos
    - Captura a saída (classe e probabilidades)
"""

import sys
import joblib
import pandas as pd


def prever_potencia(corrente_max, corrente_min, corrente_media):
    """
    Carrega o modelo e faz predição de regime de potência.

    Parâmetros:
    -----------
    corrente_max : float
        Corrente máxima medida (Amperes)
    corrente_min : float
        Corrente mínima medida (Amperes)
    corrente_media : float
        Corrente média medida (Amperes)

    Retorna:
    --------
    classe : int
        0 = Baixa Potência, 1 = Alta Potência
    prob_baixa : float
        Probabilidade de Baixa Potência (0-1)
    prob_alta : float
        Probabilidade de Alta Potência (0-1)
    """
    # Carregar modelo
    modelo = joblib.load("modelo_svm_potencia.sav")

    # Calcular atributos derivados
    amplitude = corrente_max - corrente_min
    razao = corrente_max / (corrente_media + 1e-6)

    # Criar DataFrame com ordem correta das colunas
    entrada = pd.DataFrame(
        [[corrente_max, corrente_min, corrente_media, amplitude, razao]],
        columns=[
            "corrente_max_A",
            "corrente_min_A",
            "corrente_media_A",
            "amplitude_corrente",
            "razao_max_media",
        ],
    )

    # Predição
    classe = int(modelo.predict(entrada)[0])
    probabilidades = modelo.predict_proba(entrada)[0]

    prob_baixa = float(probabilidades[0])
    prob_alta = float(probabilidades[1])

    return classe, prob_baixa, prob_alta


def main():
    """Função principal para uso via linha de comando."""

    # Verificar argumentos
    if len(sys.argv) != 4:
        print("ERRO: Número incorreto de argumentos!")
        print("\nUso:")
        print("  python usar_modelo.py <corrente_max> <corrente_min> <corrente_media>")
        print("\nExemplo:")
        print("  python usar_modelo.py 1.80 -0.03 0.67")
        sys.exit(1)

    try:
        # Ler argumentos
        corrente_max = float(sys.argv[1])
        corrente_min = float(sys.argv[2])
        corrente_media = float(sys.argv[3])

        # Fazer predição
        classe, prob_baixa, prob_alta = prever_potencia(
            corrente_max, corrente_min, corrente_media
        )

        # Saída formatada para LabVIEW
        # Formato: CLASSE|PROB_BAIXA|PROB_ALTA|NOME_CLASSE
        nome_classe = "Baixa Potência" if classe == 0 else "Alta Potência"

        print(f"{classe}|{prob_baixa:.6f}|{prob_alta:.6f}|{nome_classe}")

    except FileNotFoundError:
        print("ERRO: Arquivo 'modelo_svm_potencia.sav' não encontrado!")
        print("Execute o notebook primeiro para gerar o modelo.")
        sys.exit(1)

    except ValueError as e:
        print(f"ERRO: Valores inválidos! {e}")
        sys.exit(1)

    except Exception as e:
        print(f"ERRO: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
