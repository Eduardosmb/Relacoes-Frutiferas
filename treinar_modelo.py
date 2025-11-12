"""
Script para treinar modelo de classificação de potência elétrica
e salvá-lo em formato .sav para integração com LabVIEW

Autor: APS 1 - Projeto de Aprendizado de Máquina
Data: 2025
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("TREINAMENTO DO MODELO - CLASSIFICAÇÃO DE POTÊNCIA ELÉTRICA")
print("="*70)

# ============================================================================
# 1. CARREGAR E PRÉ-PROCESSAR DADOS
# ============================================================================
print("\n[1/5] Carregando dataset...")

caminho = "dataset.xls"
colunas = ['potencia', 'corrente_max_A', 'corrente_min_A', 'corrente_media_A']
df = pd.read_csv(caminho, header=None, names=colunas)

print(f"   ✓ Dataset carregado: {df.shape[0]} amostras, {df.shape[1]} colunas")
print(f"   ✓ Distribuição de classes:")
print(f"      - Baixa Potência (0): {(df['potencia']==0).sum()} amostras")
print(f"      - Alta Potência (1): {(df['potencia']==1).sum()} amostras")

# ============================================================================
# 2. ENGENHARIA DE ATRIBUTOS
# ============================================================================
print("\n[2/5] Criando atributos derivados...")

# Criar atributos derivados
df["amplitude_corrente"] = df["corrente_max_A"] - df["corrente_min_A"]
df["razao_max_media"] = df["corrente_max_A"] / (df["corrente_media_A"] + 1e-6)

print(f"   ✓ Atributos criados: amplitude_corrente, razao_max_media")

# Separar features e target
X = df.drop(columns=["potencia"])
y = df["potencia"]

print(f"   ✓ Features (X): {X.shape}")
print(f"   ✓ Target (y): {y.shape}")
print(f"\n   Atributos utilizados:")
for i, col in enumerate(X.columns, 1):
    print(f"      {i}. {col}")

# ============================================================================
# 3. TREINAR MODELO
# ============================================================================
print("\n[3/5] Treinando modelo SVM Linear...")

# Criar pipeline com StandardScaler + SVM
modelo = make_pipeline(
    StandardScaler(),
    SVC(kernel="linear", C=1, probability=True, random_state=42)
)

# Validação cruzada para avaliar desempenho
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(modelo, X, y, cv=cv, scoring="f1")

print(f"   ✓ Validação cruzada (5-fold):")
print(f"      - F1-score médio: {scores.mean():.4f}")
print(f"      - Desvio padrão: {scores.std():.4f}")
print(f"      - Scores individuais: {[f'{s:.4f}' for s in scores]}")

# Treinar modelo final em todo o dataset
print(f"\n   Treinando modelo final em todo o dataset...")
modelo.fit(X, y)
print(f"   ✓ Modelo treinado com sucesso!")

# Avaliar no dataset completo (para referência)
y_pred = modelo.predict(X)
print(f"\n   Desempenho no dataset completo:")
print(classification_report(y, y_pred, 
                          target_names=["Baixa Potência", "Alta Potência"],
                          digits=3))

# ============================================================================
# 4. SALVAR MODELO E SCALER
# ============================================================================
print("\n[4/5] Salvando modelo...")

# Salvar modelo completo (pipeline)
modelo_filename = "modelo_potencia.sav"
joblib.dump(modelo, modelo_filename)
print(f"   ✓ Modelo salvo em: {modelo_filename}")

# Salvar também informações sobre as features para documentação
features_info = {
    'feature_names': list(X.columns),
    'n_features': X.shape[1],
    'classes': {0: "Baixa Potência", 1: "Alta Potência"},
    'model_type': 'SVM Linear (C=1)',
    'scaler_type': 'StandardScaler'
}

info_filename = "modelo_info.sav"
joblib.dump(features_info, info_filename)
print(f"   ✓ Informações do modelo salvas em: {info_filename}")

# ============================================================================
# 5. TESTAR CARREGAMENTO E PREDIÇÃO
# ============================================================================
print("\n[5/5] Testando carregamento do modelo...")

# Carregar modelo
modelo_carregado = joblib.load(modelo_filename)
print(f"   ✓ Modelo carregado com sucesso!")

# Fazer predição de teste
exemplo_teste = {
    'corrente_max_A': 1.80,
    'corrente_min_A': -0.03,
    'corrente_media_A': 0.67
}

# Criar DataFrame com exemplo
df_teste = pd.DataFrame([exemplo_teste])

# Calcular atributos derivados
df_teste['amplitude_corrente'] = df_teste['corrente_max_A'] - df_teste['corrente_min_A']
df_teste['razao_max_media'] = df_teste['corrente_max_A'] / (df_teste['corrente_media_A'] + 1e-6)

# Garantir mesma ordem de colunas
df_teste = df_teste[X.columns]

# Fazer predição
predicao = modelo_carregado.predict(df_teste)[0]
probabilidades = modelo_carregado.predict_proba(df_teste)[0]

print(f"\n   Teste de predição:")
print(f"   Entrada: {exemplo_teste}")
print(f"   Predição: {features_info['classes'][predicao]}")
print(f"   Probabilidades:")
print(f"      - Baixa Potência: {probabilidades[0]*100:.1f}%")
print(f"      - Alta Potência: {probabilidades[1]*100:.1f}%")

# ============================================================================
# RESUMO FINAL
# ============================================================================
print("\n" + "="*70)
print("TREINAMENTO CONCLUÍDO COM SUCESSO!")
print("="*70)
print(f"\nArquivos gerados:")
print(f"   1. {modelo_filename} - Modelo treinado (pipeline completo)")
print(f"   2. {info_filename} - Informações sobre o modelo")
print(f"\nPara usar no LabVIEW:")
print(f"   1. Carregue o modelo usando joblib.load('{modelo_filename}')")
print(f"   2. Prepare os dados de entrada com os 5 atributos na ordem:")
for i, col in enumerate(X.columns, 1):
    print(f"      {i}. {col}")
print(f"   3. Use modelo.predict() para classificação")
print(f"   4. Use modelo.predict_proba() para probabilidades")
print("="*70)
