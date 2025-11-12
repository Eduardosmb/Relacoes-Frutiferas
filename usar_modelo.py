"""
Script para usar o modelo treinado e fazer predições
Útil para testar antes de integrar com o LabVIEW

Autor: APS 1 - Projeto de Aprendizado de Máquina
"""

import pandas as pd
import joblib
import warnings
warnings.filterwarnings('ignore')


def classificar_potencia(corrente_max, corrente_min, corrente_media, modelo_path="modelo_potencia.sav"):
    """
    Classifica o regime de potência baseado em medições de corrente
    
    Parâmetros:
    -----------
    corrente_max : float
        Corrente máxima observada (A)
    corrente_min : float
        Corrente mínima observada (A)
    corrente_media : float
        Corrente média calculada (A)
    modelo_path : str
        Caminho para o arquivo do modelo (.sav)
    
    Retorna:
    --------
    resultado : dict
        Dicionário com classe prevista e probabilidades
    """
    
    # Carregar modelo
    modelo = joblib.load(modelo_path)
    
    # Preparar dados de entrada
    dados = {
        'corrente_max_A': corrente_max,
        'corrente_min_A': corrente_min,
        'corrente_media_A': corrente_media
    }
    
    # Criar DataFrame
    df = pd.DataFrame([dados])
    
    # Calcular atributos derivados (mesma ordem do treinamento)
    df['amplitude_corrente'] = df['corrente_max_A'] - df['corrente_min_A']
    df['razao_max_media'] = df['corrente_max_A'] / (df['corrente_media_A'] + 1e-6)
    
    # Ordenar colunas (importante!)
    df = df[['corrente_max_A', 'corrente_min_A', 'corrente_media_A', 
             'amplitude_corrente', 'razao_max_media']]
    
    # Fazer predição
    classe = modelo.predict(df)[0]
    probabilidades = modelo.predict_proba(df)[0]
    
    # Mapear classe para nome
    classes_map = {0: "Baixa Potência", 1: "Alta Potência"}
    
    resultado = {
        'classe_numerica': int(classe),
        'classe_nome': classes_map[classe],
        'prob_baixa': float(probabilidades[0]),
        'prob_alta': float(probabilidades[1]),
        'confianca': float(max(probabilidades))
    }
    
    return resultado


def classificar_lote(dados_csv, modelo_path="modelo_potencia.sav", output_csv="predicoes.csv"):
    """
    Classifica múltiplas amostras de um arquivo CSV
    
    Parâmetros:
    -----------
    dados_csv : str
        Caminho para CSV com colunas: corrente_max_A, corrente_min_A, corrente_media_A
    modelo_path : str
        Caminho para o arquivo do modelo
    output_csv : str
        Caminho para salvar resultados
    """
    
    # Carregar dados
    df = pd.read_csv(dados_csv)
    
    # Carregar modelo
    modelo = joblib.load(modelo_path)
    
    # Calcular atributos derivados
    df['amplitude_corrente'] = df['corrente_max_A'] - df['corrente_min_A']
    df['razao_max_media'] = df['corrente_max_A'] / (df['corrente_media_A'] + 1e-6)
    
    # Preparar features
    X = df[['corrente_max_A', 'corrente_min_A', 'corrente_media_A', 
            'amplitude_corrente', 'razao_max_media']]
    
    # Fazer predições
    predicoes = modelo.predict(X)
    probabilidades = modelo.predict_proba(X)
    
    # Adicionar resultados ao DataFrame
    df['predicao_classe'] = predicoes
    df['predicao_nome'] = ['Baixa Potência' if p == 0 else 'Alta Potência' for p in predicoes]
    df['prob_baixa'] = probabilidades[:, 0]
    df['prob_alta'] = probabilidades[:, 1]
    df['confianca'] = probabilidades.max(axis=1)
    
    # Salvar resultados
    df.to_csv(output_csv, index=False)
    print(f"Predições salvas em: {output_csv}")
    
    return df


# ============================================================================
# EXEMPLO DE USO
# ============================================================================
if __name__ == "__main__":
    print("="*70)
    print("TESTE DO MODELO DE CLASSIFICAÇÃO DE POTÊNCIA")
    print("="*70)
    
    # Exemplo 1: Predição única
    print("\n[Teste 1] Predição única:")
    print("-" * 70)
    
    resultado = classificar_potencia(
        corrente_max=1.80,
        corrente_min=-0.03,
        corrente_media=0.67
    )
    
    print(f"Entrada:")
    print(f"   Corrente Máxima: 1.80 A")
    print(f"   Corrente Mínima: -0.03 A")
    print(f"   Corrente Média: 0.67 A")
    print(f"\nResultado:")
    print(f"   Classe: {resultado['classe_nome']} ({resultado['classe_numerica']})")
    print(f"   Confiança: {resultado['confianca']*100:.1f}%")
    print(f"   Probabilidades:")
    print(f"      - Baixa Potência: {resultado['prob_baixa']*100:.1f}%")
    print(f"      - Alta Potência: {resultado['prob_alta']*100:.1f}%")
    
    # Exemplo 2: Mais testes
    print("\n" + "-" * 70)
    print("[Teste 2] Múltiplas predições:")
    print("-" * 70)
    
    testes = [
        (1.80, -0.03, 0.67),   # Teste 1
        (10.70, -0.03, 0.67),  # Teste 2
        (1.76, -0.03, 0.66),   # Teste 3
    ]
    
    for i, (c_max, c_min, c_med) in enumerate(testes, 1):
        resultado = classificar_potencia(c_max, c_min, c_med)
        print(f"\nTeste {i}: max={c_max}, min={c_min}, med={c_med}")
        print(f"   → {resultado['classe_nome']} (confiança: {resultado['confianca']*100:.1f}%)")
    
    print("\n" + "="*70)
    print("TESTES CONCLUÍDOS!")
    print("="*70)
    print("\nPara usar no LabVIEW:")
    print("   1. Chame a função classificar_potencia() com os 3 valores de corrente")
    print("   2. O retorno inclui a classe prevista e probabilidades")
    print("   3. Use 'classe_numerica' para decisões (0 ou 1)")
    print("   4. Use 'confianca' para avaliar certeza da predição")
    print("="*70)
