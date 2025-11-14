import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import os
import joblib

def Modelar_Salvar_DTC():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1, shuffle=True)
    
    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    
    # Salvar o modelo treinado em um arquivo .sav
    joblib.dump(dtc, 'modelo_classificador_dtc.sav')
    return()



def CarregarModelo_Predicao(A, B, C, D):  
    X_test = np.array([[A, B, C, D]])
    
    # Carregar o modelo treinado salvo em arquivo .sav
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'modelo_classificador_dtc.sav')
    ModeloCarregado = joblib.load(model_path)
    
    y_pred = ModeloCarregado.predict(X_test)
    return y_pred[0]


# Chamadas das funções para testes:

# ***** Teste para modelar e salvar objeto :   
#Modelar_Salvar_DTC()

# ***** Teste para carregar e fazer predição:
#resultado = CarregarModelo_Predicao(5.1, 3.5, 1.4, 0.2)
#print("Classe prevista:", resultado)

