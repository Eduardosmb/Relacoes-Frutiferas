# 🚀 Guia Rápido: Integração Python 3.6 + LabVIEW

## 📦 Arquivos Disponíveis para LabVIEW

| Arquivo | Descrição | Uso Recomendado |
|---------|-----------|-----------------|
| **modelo_svm_potencia.sav** | Modelo treinado (2.7 KB) | Carregado pelos scripts Python |
| **predicao_labview.py** | Script minimalista | System Exec.vi (linha de comando) |
| **modelo_predicao.py** | Módulo completo | Python Node ou System Exec.vi |
| **exemplo_uso_modelo.py** | Exemplos de uso | Aprendizado e testes |

---

## 🔧 Método 1: System Exec.vi (MAIS SIMPLES)

### Configuração no LabVIEW:

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Arrastar "System Exec.vi" para o diagrama                    │
│ 2. Conectar entradas:                                            │
│    - command line: string com comando Python                     │
│    - timeout (ms): 10000 (10 segundos)                          │
│ 3. Conectar saídas:                                              │
│    - standard output: string com resultado                       │
│    - return code: 0 = sucesso, != 0 = erro                      │
└─────────────────────────────────────────────────────────────────┘
```

### Exemplo de Comando:

```bash
python3 /caminho/completo/predicao_labview.py 1.80 -0.03 0.67
```

### Saída Esperada:

```
1|0.008372|0.991628
```

Formato: `CLASSE|PROB_BAIXA|PROB_ALTA`

### Parsing no LabVIEW:

```
┌──────────────────────────────────────────────────────────────┐
│  [standard output] → [Spreadsheet String to Array]           │
│                                                               │
│  Configurações:                                               │
│    - Delimiter: "|"                                          │
│    - Format: %f (float)                                      │
│                                                               │
│  Saída (Array de 3 elementos):                               │
│    - Array[0] = Classe (0 ou 1)                             │
│    - Array[1] = Probabilidade Baixa (0-1)                   │
│    - Array[2] = Probabilidade Alta (0-1)                    │
└──────────────────────────────────────────────────────────────┘
```

### Diagrama de Blocos Exemplo:

```
┌─────────────┐
│  corrente_  │
│  max (DBL)  │────┐
└─────────────┘    │
                   │    ┌──────────────────┐
┌─────────────┐    ├───→│                  │
│  corrente_  │    │    │  Format Into     │    ┌─────────────────┐
│  min (DBL)  │────┤    │  String          │───→│                 │
└─────────────┘    │    │                  │    │  System Exec.vi │
                   │    │  Format: "python3│    │                 │
┌─────────────┐    │    │  predicao_lab... │    └────────┬────────┘
│  corrente_  │    │    │  %.2f %.2f %.2f" │             │
│  media(DBL) │────┘    └──────────────────┘             │
└─────────────┘                                           │
                                                          │
                                              ┌───────────▼────────────┐
                                              │ Spreadsheet String to │
                                              │ Array                 │
                                              │ Delimiter: "|"        │
                                              └───────────┬───────────┘
                                                          │
                                    ┌─────────────────────┼─────────────────────┐
                                    │                     │                     │
                              ┌─────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
                              │  Index     │      │   Index     │      │   Index     │
                              │  Array[0]  │      │   Array[1]  │      │   Array[2]  │
                              └─────┬──────┘      └──────┬──────┘      └──────┬──────┘
                                    │                    │                     │
                              ┌─────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
                              │  classe    │      │  prob_baixa │      │  prob_alta  │
                              │  (I32)     │      │  (DBL)      │      │  (DBL)      │
                              └────────────┘      └─────────────┘      └─────────────┘
```

---

## 🐍 Método 2: Python Node (LabVIEW 2018+)

### Requisitos:

- LabVIEW 2018 ou superior
- Python 3.6+ configurado no LabVIEW

### Configuração:

1. **Arrastar "Python Node"** para o diagrama
2. **Configurar Python Node:**
   - Script: `modelo_predicao.py`
   - Função: `prever`
3. **Conectar entradas** (3 DBL):
   - corrente_max
   - corrente_min
   - corrente_media
4. **Conectar saídas** (tuple de 3 elementos):
   - classe (I32)
   - prob_baixa (DBL)
   - prob_alta (DBL)

### Vantagens:

✅ Mais rápido (não precisa iniciar Python toda vez)  
✅ Integração nativa com tipos LabVIEW  
✅ Melhor para loops de aquisição contínua

---

## 📝 Exemplos Práticos

### Exemplo 1: Predição Única

**Entrada:**
- corrente_max = 1.80 A
- corrente_min = -0.03 A
- corrente_media = 0.67 A

**Comando:**
```bash
python3 predicao_labview.py 1.80 -0.03 0.67
```

**Saída:**
```
1|0.008372|0.991628
```

**Interpretação:**
- Classe: **1** (Alta Potência)
- Probabilidade Baixa: **0.84%**
- Probabilidade Alta: **99.16%**

---

### Exemplo 2: Predição em Loop (Monitoramento Contínuo)

```
┌─────────────────────────────────────────────────────────────┐
│  WHILE LOOP                                                  │
│                                                              │
│  ┌──────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │ Ler DAQ  │ ───→ │ Calcular     │ ───→ │ Python Node  │ │
│  │ (3 Ch)   │      │ Max/Min/Média│      │ ou           │ │
│  └──────────┘      └──────────────┘      │ System Exec  │ │
│                                           └──────┬───────┘ │
│                                                  │         │
│                                           ┌──────▼───────┐ │
│                                           │ Exibir       │ │
│                                           │ Resultado    │ │
│                                           └──────────────┘ │
│                                                            │
│  ┌──────────┐                                             │
│  │ Wait (ms)│ ← 1000 (atualizar a cada 1 segundo)        │
│  └──────────┘                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 Como Testar

### Teste 1: Via Terminal (antes de integrar com LabVIEW)

```bash
# Teste Alta Potência
python3 predicao_labview.py 1.80 -0.03 0.67
# Esperado: 1|0.008372|0.991628

# Teste Baixa Potência
python3 predicao_labview.py 1.13 -0.01 0.47
# Esperado: 0|0.968584|0.031416
```

### Teste 2: Usando Exemplo Completo

```bash
python3 exemplo_uso_modelo.py
```

Mostra 5 exemplos de uso com diferentes cenários.

---

## 🔍 Troubleshooting

### Problema 1: "comando não encontrado"

**Solução:** Usar caminho absoluto do Python:
```
/usr/local/bin/python3 /caminho/completo/predicao_labview.py ...
```

No Mac, encontrar o caminho:
```bash
which python3
```

### Problema 2: "modelo_svm_potencia.sav não encontrado"

**Solução 1:** Usar caminho absoluto no código Python:
```python
CAMINHO_MODELO = "/Users/enzo/Desktop/ia/Relacoes-Frutiferas/modelo_svm_potencia.sav"
```

**Solução 2:** Definir working directory no System Exec.vi:
- Clicar com botão direito → Properties
- Execution → Working Directory
- Definir para: `/Users/enzo/Desktop/ia/Relacoes-Frutiferas`

### Problema 3: Timeout Error

**Solução:** Aumentar timeout no System Exec.vi:
- Padrão: 10000 ms (10 segundos)
- Recomendado: 30000 ms (30 segundos) para primeira execução
- Depois: 5000 ms (5 segundos) é suficiente

### Problema 4: Erro de parsing

**Verificar:**
- Delimitador está configurado como `|` (pipe)
- Formato está como `%f` ou deixar automático
- Não há espaços extras na saída

---

## 📊 Valores de Referência

### Limiar de Decisão

O modelo decide baseado principalmente na **corrente média**:

| Corrente Média | Classe Esperada | Confiança Típica |
|----------------|----------------|------------------|
| < 0.49 A | Baixa Potência | > 95% |
| 0.49 - 0.555 A | Baixa (limiar) | 50-90% |
| 0.555 - 0.62 A | Alta (limiar) | 50-90% |
| > 0.62 A | Alta Potência | > 95% |

### Zona de Transição (0.49 - 0.62 A)

Nesta faixa, o modelo pode ter menor confiança. Considere:
- Adicionar **histerese** no LabVIEW
- Fazer **média de 3-5 leituras** antes de decidir
- Usar **probabilidade** além da classe

---

## 💡 Dicas de Otimização

### 1. Carregar Modelo Uma Vez

Em vez de carregar o modelo toda vez, **carregue uma vez** no início:

**Python com cache:**
```python
_modelo_cache = None

def prever_cached(max, min, media):
    global _modelo_cache
    if _modelo_cache is None:
        _modelo_cache = joblib.load("modelo_svm_potencia.sav")
    # ... usar _modelo_cache
```

### 2. Processamento em Lote

Para múltiplas amostras, processar em lote é mais rápido:

```python
# Em vez de chamar prever() 10 vezes
# Passar todas as 10 amostras de uma vez
entrada_batch = pd.DataFrame([
    [max1, min1, med1, amp1, raz1],
    [max2, min2, med2, amp2, raz2],
    # ...
])
classes = modelo.predict(entrada_batch)
```

### 3. Filtro de Ruído no LabVIEW

Adicione um **filtro passa-baixa** antes de enviar para o Python:
- Média móvel de 5-10 amostras
- Reduz ruído nos sensores
- Melhora estabilidade da classificação

---

## 🎯 Resumo de Comandos

```bash
# Predição simples
python3 predicao_labview.py 1.80 -0.03 0.67

# Predição com módulo completo
python3 modelo_predicao.py 1.80 -0.03 0.67

# Executar exemplos
python3 exemplo_uso_modelo.py

# Testar integração completa
python3 teste_integracao.py
```

---

## ✅ Checklist Final

- [ ] Python 3.6+ instalado
- [ ] Bibliotecas instaladas (sklearn, pandas, joblib)
- [ ] Arquivo `modelo_svm_potencia.sav` no lugar correto
- [ ] Script Python testado via terminal
- [ ] System Exec.vi configurado no LabVIEW
- [ ] Parsing da saída funcionando
- [ ] Teste com valores conhecidos OK
- [ ] Integração com DAQ implementada

---

**🚀 Agora você está pronto para integrar o modelo com LabVIEW!**

Para mais detalhes, consulte:
- `LABVIEW_INTEGRATION.md` - Guia completo
- `exemplo_uso_modelo.py` - Exemplos práticos
- `teste_integracao.py` - Testes automatizados

