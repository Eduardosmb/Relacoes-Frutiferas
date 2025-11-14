import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import os
import joblib


def Modelar_Salvar_SVM():
    """
    Treina o modelo SVM Linear com o dataset de potência e salva em .sav
    """
    # Carregar dataset
    colunas = ["potencia", "corrente_max_A", "corrente_min_A", "corrente_media_A"]
    df = pd.read_csv("dataset.xls", header=None, names=colunas)

    # Adicionar atributos derivados
    df["amplitude_corrente"] = df["corrente_max_A"] - df["corrente_min_A"]
    df["razao_max_media"] = df["corrente_max_A"] / (df["corrente_media_A"] + 1e-6)

    # Preparar dados
    X = df[
        [
            "corrente_max_A",
            "corrente_min_A",
            "corrente_media_A",
            "amplitude_corrente",
            "razao_max_media",
        ]
    ]
    y = df["potencia"]

    # Criar e treinar pipeline (StandardScaler + SVM Linear)
    modelo_svm = make_pipeline(
        StandardScaler(), SVC(kernel="linear", C=1, probability=True, random_state=42)
    )
    modelo_svm.fit(X, y)

    # Salvar o modelo treinado em um arquivo .sav
    joblib.dump(modelo_svm, "modelo_svm_potencia.sav")
    return ()


def CarregarModelo_Predicao(corrente_max, corrente_min, corrente_media):
    """
    Carrega o modelo treinado e faz predição de regime de potência.

    Parâmetros:
        corrente_max: Corrente máxima (A)
        corrente_min: Corrente mínima (A)
        corrente_media: Corrente média (A)

    Retorna:
        classe: 0 = Baixa Potência, 1 = Alta Potência
    """
    # Calcular atributos derivados
    amplitude = corrente_max - corrente_min
    razao = corrente_max / (corrente_media + 1e-6)

    # Criar array de entrada com os 5 atributos
    X_test = np.array([[corrente_max, corrente_min, corrente_media, amplitude, razao]])

    # Criar DataFrame com nomes das colunas
    X_test_df = pd.DataFrame(
        X_test,
        columns=[
            "corrente_max_A",
            "corrente_min_A",
            "corrente_media_A",
            "amplitude_corrente",
            "razao_max_media",
        ],
    )

    # Carregar o modelo treinado salvo em arquivo .sav
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "modelo_svm_potencia.sav")
    ModeloCarregado = joblib.load(model_path)

    # Fazer predição
    y_pred = ModeloCarregado.predict(X_test_df)
    return y_pred[0]


def CarregarModelo_Predicao_Completa(corrente_max, corrente_min, corrente_media):
    """
    Carrega o modelo e faz predição retornando classe e probabilidades.

    Parâmetros:
        corrente_max: Corrente máxima (A)
        corrente_min: Corrente mínima (A)
        corrente_media: Corrente média (A)

    Retorna:
        classe: 0 = Baixa Potência, 1 = Alta Potência
        prob_baixa: Probabilidade de Baixa Potência (0-1)
        prob_alta: Probabilidade de Alta Potência (0-1)
    """
    # Calcular atributos derivados
    amplitude = corrente_max - corrente_min
    razao = corrente_max / (corrente_media + 1e-6)

    # Criar array de entrada
    X_test = np.array([[corrente_max, corrente_min, corrente_media, amplitude, razao]])

    # Criar DataFrame com nomes das colunas
    X_test_df = pd.DataFrame(
        X_test,
        columns=[
            "corrente_max_A",
            "corrente_min_A",
            "corrente_media_A",
            "amplitude_corrente",
            "razao_max_media",
        ],
    )

    # Carregar o modelo treinado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "modelo_svm_potencia.sav")
    ModeloCarregado = joblib.load(model_path)

    # Fazer predição
    y_pred = ModeloCarregado.predict(X_test_df)
    y_proba = ModeloCarregado.predict_proba(X_test_df)

    classe = int(y_pred[0])
    prob_baixa = float(y_proba[0][0])
    prob_alta = float(y_proba[0][1])

    return classe, prob_baixa, prob_alta


# Chamadas das funções para testes:

# ***** Teste para modelar e salvar objeto:
# Modelar_Salvar_SVM()

# ***** Teste para carregar e fazer predição (apenas classe):
# resultado = CarregarModelo_Predicao(1.80, -0.03, 0.67)
# print("Classe prevista:", resultado)

# ***** Teste para carregar e fazer predição (completa):
# classe, prob_baixa, prob_alta = CarregarModelo_Predicao_Completa(1.80, -0.03, 0.67)
# print("Classe prevista:", classe)
# print("Probabilidade Baixa:", prob_baixa)
# print("Probabilidade Alta:", prob_alta)
