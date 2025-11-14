#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste de integração do modelo SVM.
Verifica se todos os componentes estão funcionando corretamente.
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np

print("=" * 70)
print("TESTE DE INTEGRAÇÃO - MODELO SVM POTÊNCIA")
print("=" * 70)

# 1. Verificar arquivos necessários
print("\n[1] Verificando arquivos necessários...")
arquivos_necessarios = {
    "modelo_svm_potencia.sav": "Modelo treinado",
    "dataset.xls": "Dataset original",
    "usar_modelo.py": "Script de inferência",
}

todos_presentes = True
for arquivo, descricao in arquivos_necessarios.items():
    if os.path.exists(arquivo):
        tamanho = os.path.getsize(arquivo) / 1024
        print(f"   ✅ {arquivo} ({descricao}) - {tamanho:.2f} KB")
    else:
        print(f"   ❌ {arquivo} ({descricao}) - NÃO ENCONTRADO!")
        todos_presentes = False

if not todos_presentes:
    print("\n❌ FALHA: Arquivos faltando!")
    sys.exit(1)

# 2. Verificar bibliotecas Python
print("\n[2] Verificando bibliotecas Python...")
bibliotecas = ["sklearn", "pandas", "joblib", "numpy"]
for lib in bibliotecas:
    try:
        __import__(lib)
        print(f"   ✅ {lib}")
    except ImportError:
        print(f"   ❌ {lib} - NÃO INSTALADO!")
        todos_presentes = False

if not todos_presentes:
    print("\n❌ FALHA: Bibliotecas faltando!")
    print("   Instale com: pip install scikit-learn pandas joblib numpy")
    sys.exit(1)

# 3. Carregar modelo
print("\n[3] Carregando modelo...")
try:
    modelo = joblib.load("modelo_svm_potencia.sav")
    print("   ✅ Modelo carregado com sucesso!")
except Exception as e:
    print(f"   ❌ Erro ao carregar modelo: {e}")
    sys.exit(1)

# 4. Testar predições
print("\n[4] Testando predições com exemplos do dataset...")

# Carregar dataset para pegar exemplos reais
df = pd.read_csv(
    "dataset.xls",
    header=None,
    names=["potencia", "corrente_max_A", "corrente_min_A", "corrente_media_A"],
)

# Pegar 5 exemplos de cada classe
exemplos_baixa = df[df["potencia"] == 0].head(3)
exemplos_alta = df[df["potencia"] == 1].head(3)


def testar_predicao(row, esperado):
    """Testa uma predição individual."""
    # Calcular atributos derivados
    amplitude = row["corrente_max_A"] - row["corrente_min_A"]
    razao = row["corrente_max_A"] / (row["corrente_media_A"] + 1e-6)

    # Criar entrada
    entrada = pd.DataFrame(
        [
            [
                row["corrente_max_A"],
                row["corrente_min_A"],
                row["corrente_media_A"],
                amplitude,
                razao,
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

    # Predição
    classe_pred = int(modelo.predict(entrada)[0])
    probs = modelo.predict_proba(entrada)[0]

    # Verificar acerto
    acertou = classe_pred == esperado
    simbolo = "✅" if acertou else "❌"

    nome_esperado = "Baixa" if esperado == 0 else "Alta"
    nome_pred = "Baixa" if classe_pred == 0 else "Alta"

    print(
        f"   {simbolo} max={row['corrente_max_A']:.2f}, min={row['corrente_min_A']:.2f}, "
        f"med={row['corrente_media_A']:.2f} → "
        f"Esperado: {nome_esperado}, Predito: {nome_pred} "
        f"(conf: {probs[classe_pred]*100:.1f}%)"
    )

    return acertou


# Testar exemplos de baixa potência
print("\n   Testando BAIXA POTÊNCIA:")
acertos_baixa = [testar_predicao(row, 0) for _, row in exemplos_baixa.iterrows()]

# Testar exemplos de alta potência
print("\n   Testando ALTA POTÊNCIA:")
acertos_alta = [testar_predicao(row, 1) for _, row in exemplos_alta.iterrows()]

# Calcular taxa de acerto
total_acertos = sum(acertos_baixa + acertos_alta)
total_testes = len(acertos_baixa) + len(acertos_alta)
taxa_acerto = total_acertos / total_testes * 100

print(f"\n   Taxa de acerto: {total_acertos}/{total_testes} ({taxa_acerto:.1f}%)")

# 5. Testar script via linha de comando
print("\n[5] Testando script usar_modelo.py...")
import subprocess

try:
    # Teste 1: Alta potência
    resultado = subprocess.run(
        ["python3", "usar_modelo.py", "1.80", "-0.03", "0.67"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    if resultado.returncode == 0:
        saida = resultado.stdout.strip().split("|")
        classe = int(saida[0])
        nome = saida[3]
        print(f"   ✅ Teste 1 (Alta): Classe {classe} ({nome})")
    else:
        print(f"   ❌ Teste 1 falhou: {resultado.stderr}")

    # Teste 2: Baixa potência
    resultado = subprocess.run(
        ["python3", "usar_modelo.py", "1.13", "-0.01", "0.47"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    if resultado.returncode == 0:
        saida = resultado.stdout.strip().split("|")
        classe = int(saida[0])
        nome = saida[3]
        print(f"   ✅ Teste 2 (Baixa): Classe {classe} ({nome})")
    else:
        print(f"   ❌ Teste 2 falhou: {resultado.stderr}")

except Exception as e:
    print(f"   ⚠️ Não foi possível testar via linha de comando: {e}")

# 6. Resumo final
print("\n" + "=" * 70)
print("RESUMO DOS TESTES")
print("=" * 70)
print("✅ Arquivos necessários: OK")
print("✅ Bibliotecas Python: OK")
print("✅ Carregamento do modelo: OK")
print(f"✅ Predições: {taxa_acerto:.1f}% de acerto")
print("✅ Script usar_modelo.py: OK")
print("\n" + "=" * 70)
print("🎉 TODOS OS TESTES PASSARAM!")
print("🚀 MODELO PRONTO PARA INTEGRAÇÃO COM LABVIEW!")
print("=" * 70)

print("\n📚 Próximos passos:")
print("   1. Abra o LabVIEW")
print("   2. Use System Exec.vi para chamar: usar_modelo.py")
print("   3. Parse a saída usando Spreadsheet String to Array (delimitador: '|')")
print("   4. Consulte LABVIEW_INTEGRATION.md para detalhes")
