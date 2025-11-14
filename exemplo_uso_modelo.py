#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplos de uso do modelo de predição de potência.
Demonstra diferentes formas de integração com LabVIEW.
"""

import modelo_predicao as mp


print("=" * 70)
print("EXEMPLOS DE USO DO MODELO DE PREDIÇÃO")
print("=" * 70)


# ==============================================================================
# EXEMPLO 1: Uso básico da função prever()
# ==============================================================================
print("\n[EXEMPLO 1] Uso básico - função prever()")
print("-" * 70)

corrente_max = 1.80
corrente_min = -0.03
corrente_media = 0.67

classe, prob_baixa, prob_alta = mp.prever(corrente_max, corrente_min, corrente_media)

print("Entrada:")
print("  Corrente máxima:  {:.2f} A".format(corrente_max))
print("  Corrente mínima:  {:.2f} A".format(corrente_min))
print("  Corrente média:   {:.2f} A".format(corrente_media))
print("\nSaída:")
print(
    "  Classe predita:   {} ({})".format(
        classe, "Baixa Potência" if classe == 0 else "Alta Potência"
    )
)
print("  Prob. Baixa:      {:.2%}".format(prob_baixa))
print("  Prob. Alta:       {:.2%}".format(prob_alta))


# ==============================================================================
# EXEMPLO 2: Uso da função prever_detalhado()
# ==============================================================================
print("\n\n[EXEMPLO 2] Uso avançado - função prever_detalhado()")
print("-" * 70)

corrente_max = 1.13
corrente_min = -0.01
corrente_media = 0.47

resultado = mp.prever_detalhado(corrente_max, corrente_min, corrente_media)

print("Entrada:")
print("  Corrente máxima:  {:.2f} A".format(corrente_max))
print("  Corrente mínima:  {:.2f} A".format(corrente_min))
print("  Corrente média:   {:.2f} A".format(corrente_media))
print("\nSaída completa:")
print("  Classe:           {}".format(resultado["classe"]))
print("  Nome:             {}".format(resultado["nome_classe"]))
print("  Confiança:        {:.2%}".format(resultado["confianca"]))
print("  Prob. Baixa:      {:.2%}".format(resultado["prob_baixa"]))
print("  Prob. Alta:       {:.2%}".format(resultado["prob_alta"]))
print("\nAtributos derivados:")
print("  Amplitude:        {:.4f}".format(resultado["amplitude"]))
print("  Razão max/média:  {:.4f}".format(resultado["razao"]))


# ==============================================================================
# EXEMPLO 3: Múltiplas predições (simulando monitoramento contínuo)
# ==============================================================================
print("\n\n[EXEMPLO 3] Múltiplas predições (monitoramento contínuo)")
print("-" * 70)

# Simular 5 leituras de sensores
leituras = [
    (1.77, -0.03, 0.67, "Alta esperada"),
    (1.13, -0.01, 0.47, "Baixa esperada"),
    (1.80, -0.06, 0.66, "Alta esperada"),
    (1.08, -0.01, 0.46, "Baixa esperada"),
    (1.71, -0.01, 0.64, "Alta esperada"),
]

print(
    "\n{:<6} {:<8} {:<8} {:<8} {:<20} {:<10}".format(
        "Nº", "Max", "Min", "Média", "Classe Predita", "Confiança"
    )
)
print("-" * 70)

for i, (max_v, min_v, med_v, esperada) in enumerate(leituras, 1):
    classe, prob_baixa, prob_alta = mp.prever(max_v, min_v, med_v)
    nome_classe = "Baixa Potência" if classe == 0 else "Alta Potência"
    confianca = prob_baixa if classe == 0 else prob_alta

    print(
        "{:<6} {:<8.2f} {:<8.2f} {:<8.2f} {:<20} {:<10.1%}".format(
            i, max_v, min_v, med_v, nome_classe, confianca
        )
    )


# ==============================================================================
# EXEMPLO 4: Detecção de mudança de regime
# ==============================================================================
print("\n\n[EXEMPLO 4] Detecção de mudança de regime operacional")
print("-" * 70)

# Simular transição de baixa para alta potência
leituras_transicao = [
    (1.10, -0.01, 0.46),  # Baixa
    (1.12, -0.01, 0.47),  # Baixa
    (1.15, -0.01, 0.48),  # Baixa (próximo ao limite)
    (1.50, 0.00, 0.55),  # Zona de transição
    (1.70, -0.02, 0.63),  # Alta
    (1.75, -0.03, 0.65),  # Alta
]

regime_anterior = None

print(
    "\n{:<6} {:<10} {:<20} {:<10} {:<15}".format(
        "Nº", "Corrente", "Regime", "Confiança", "Status"
    )
)
print("-" * 70)

for i, (max_v, min_v, med_v) in enumerate(leituras_transicao, 1):
    classe, prob_baixa, prob_alta = mp.prever(max_v, min_v, med_v)
    nome_classe = "Baixa" if classe == 0 else "Alta"
    confianca = prob_baixa if classe == 0 else prob_alta

    # Detectar mudança de regime
    if regime_anterior is not None and regime_anterior != classe:
        status = "⚠️ MUDANÇA!"
    else:
        status = "✓ Estável"

    print(
        "{:<6} {:<10.2f} {:<20} {:<10.1%} {:<15}".format(
            i, med_v, nome_classe + " Potência", confianca, status
        )
    )

    regime_anterior = classe


# ==============================================================================
# EXEMPLO 5: Integração com LabVIEW (formato de saída)
# ==============================================================================
print("\n\n[EXEMPLO 5] Formato de saída para LabVIEW System Exec.vi")
print("-" * 70)

print("\nFormato CSV com pipe (|) como delimitador:")
print("CLASSE|PROB_BAIXA|PROB_ALTA\n")

exemplos_labview = [
    (1.80, -0.03, 0.67),
    (1.13, -0.01, 0.47),
]

for max_v, min_v, med_v in exemplos_labview:
    classe, prob_baixa, prob_alta = mp.prever(max_v, min_v, med_v)
    print("{}|{:.6f}|{:.6f}".format(classe, prob_baixa, prob_alta))

print("\nParsing no LabVIEW:")
print("  1. Usar 'Spreadsheet String to Array'")
print("  2. Configurar delimitador: '|'")
print("  3. Índices: [0]=classe, [1]=prob_baixa, [2]=prob_alta")


# ==============================================================================
# RESUMO
# ==============================================================================
print("\n\n" + "=" * 70)
print("RESUMO DAS FUNÇÕES DISPONÍVEIS")
print("=" * 70)

print(
    """
1. prever(max, min, media)
   → Retorna: (classe, prob_baixa, prob_alta)
   → Uso: Predição simples e rápida
   
2. prever_detalhado(max, min, media)
   → Retorna: dict com todas as informações
   → Uso: Quando precisa de mais detalhes

3. carregar_modelo()
   → Retorna: Pipeline do sklearn
   → Uso: Carregar modelo uma vez e reutilizar

Para LabVIEW:
   - System Exec.vi: python3 modelo_predicao.py <max> <min> <media>
   - Python Node: importar função prever()
"""
)

print("=" * 70)
print("✅ Todos os exemplos executados com sucesso!")
print("=" * 70)
