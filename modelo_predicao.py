#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo Python 3.6+ para predição de potência
Compatível com LabVIEW Python Node e System Exec

Autor: Sistema de Classificação de Potência
Data: Novembro 2025
"""

import joblib
import pandas as pd
import os


# Caminho do modelo (ajustar se necessário)
CAMINHO_MODELO = "modelo_svm_potencia.sav"


def carregar_modelo():
    """
    Carrega o modelo SVM treinado usando joblib.

    Returns:
        Pipeline: Modelo sklearn Pipeline (StandardScaler + SVC)

    Raises:
        FileNotFoundError: Se o arquivo .sav não for encontrado
    """
    if not os.path.exists(CAMINHO_MODELO):
        raise FileNotFoundError("Modelo não encontrado: {}".format(CAMINHO_MODELO))

    modelo = joblib.load(CAMINHO_MODELO)
    return modelo


def prever(corrente_max, corrente_min, corrente_media):
    """
    Faz predição de regime de potência baseado em medições de corrente.

    Função compatível com LabVIEW Python Node (LabVIEW 2018+).

    Args:
        corrente_max (float): Corrente máxima medida em Amperes
        corrente_min (float): Corrente mínima medida em Amperes
        corrente_media (float): Corrente média medida em Amperes

    Returns:
        tuple: (classe, prob_baixa, prob_alta)
            - classe (int): 0 = Baixa Potência, 1 = Alta Potência
            - prob_baixa (float): Probabilidade de Baixa Potência (0-1)
            - prob_alta (float): Probabilidade de Alta Potência (0-1)

    Example:
        >>> classe, prob_baixa, prob_alta = prever(1.80, -0.03, 0.67)
        >>> print(classe)  # 1 (Alta Potência)
        >>> print(prob_alta)  # 0.991628
    """
    # Carregar modelo
    modelo = carregar_modelo()

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

    # Fazer predição
    classe = int(modelo.predict(entrada)[0])
    probs = modelo.predict_proba(entrada)[0]

    prob_baixa = float(probs[0])
    prob_alta = float(probs[1])

    return classe, prob_baixa, prob_alta


def prever_detalhado(corrente_max, corrente_min, corrente_media):
    """
    Versão detalhada da predição com informações adicionais.

    Args:
        corrente_max (float): Corrente máxima em Amperes
        corrente_min (float): Corrente mínima em Amperes
        corrente_media (float): Corrente média em Amperes

    Returns:
        dict: Dicionário com todas as informações da predição
            {
                'classe': int (0 ou 1),
                'nome_classe': str ('Baixa Potência' ou 'Alta Potência'),
                'prob_baixa': float (0-1),
                'prob_alta': float (0-1),
                'confianca': float (0-1),
                'amplitude': float,
                'razao': float
            }
    """
    classe, prob_baixa, prob_alta = prever(corrente_max, corrente_min, corrente_media)

    nome_classe = "Baixa Potência" if classe == 0 else "Alta Potência"
    confianca = prob_baixa if classe == 0 else prob_alta

    return {
        "classe": classe,
        "nome_classe": nome_classe,
        "prob_baixa": prob_baixa,
        "prob_alta": prob_alta,
        "confianca": confianca,
        "amplitude": corrente_max - corrente_min,
        "razao": corrente_max / (corrente_media + 1e-6),
    }


# ==============================================================================
# FUNÇÕES PARA USO VIA LINHA DE COMANDO (System Exec.vi)
# ==============================================================================


def main_linha_comando():
    """
    Função principal para uso via System Exec.vi do LabVIEW.

    Uso:
        python3 modelo_predicao.py <corrente_max> <corrente_min> <corrente_media>

    Saída:
        CLASSE|PROB_BAIXA|PROB_ALTA (formato CSV com pipe)
    """
    import sys

    if len(sys.argv) != 4:
        print("ERRO: 3 argumentos necessários")
        print("Uso: python3 {} <max> <min> <media>".format(sys.argv[0]))
        sys.exit(1)

    try:
        corrente_max = float(sys.argv[1])
        corrente_min = float(sys.argv[2])
        corrente_media = float(sys.argv[3])

        classe, prob_baixa, prob_alta = prever(
            corrente_max, corrente_min, corrente_media
        )

        # Saída formatada para LabVIEW
        print("{}|{:.6f}|{:.6f}".format(classe, prob_baixa, prob_alta))
        sys.exit(0)

    except Exception as e:
        print("ERRO: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    main_linha_comando()
