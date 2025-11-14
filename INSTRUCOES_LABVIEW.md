# Instruções de Integração: Python 3.6 + LabVIEW

## 📄 Arquivo Principal: `Integracao_Modelo_Potencia.py`

Baseado no padrão do arquivo `Integracao LV_Scikit-learn.py`

---

## 🔧 Funções Disponíveis

### 1️⃣ `Modelar_Salvar_SVM()`

**Descrição:** Treina o modelo SVM Linear e salva em arquivo `.sav`

**Uso:**
```python
from Integracao_Modelo_Potencia import Modelar_Salvar_SVM

# Treinar e salvar modelo
Modelar_Salvar_SVM()
```

**Saída:** Arquivo `modelo_svm_potencia.sav` (2.7 KB)

---

### 2️⃣ `CarregarModelo_Predicao(corrente_max, corrente_min, corrente_media)`

**Descrição:** Carrega o modelo e retorna apenas a classe predita

**Parâmetros:**
- `corrente_max` (float): Corrente máxima em Amperes
- `corrente_min` (float): Corrente mínima em Amperes
- `corrente_media` (float): Corrente média em Amperes

**Retorna:**
- `classe` (float): 0.0 = Baixa Potência, 1.0 = Alta Potência

**Uso no Python:**
```python
from Integracao_Modelo_Potencia import CarregarModelo_Predicao

resultado = CarregarModelo_Predicao(1.80, -0.03, 0.67)
print("Classe prevista:", resultado)  # 1.0 (Alta Potência)
```

**Uso no LabVIEW Python Node:**
```
Entradas (DBL):
  - corrente_max: 1.80
  - corrente_min: -0.03
  - corrente_media: 0.67

Saída (DBL):
  - classe: 1.0 (Alta Potência)
```

---

### 3️⃣ `CarregarModelo_Predicao_Completa(corrente_max, corrente_min, corrente_media)`

**Descrição:** Carrega o modelo e retorna classe + probabilidades

**Parâmetros:**
- `corrente_max` (float): Corrente máxima em Amperes
- `corrente_min` (float): Corrente mínima em Amperes
- `corrente_media` (float): Corrente média em Amperes

**Retorna (tuple):**
- `classe` (int): 0 = Baixa Potência, 1 = Alta Potência
- `prob_baixa` (float): Probabilidade de Baixa Potência (0-1)
- `prob_alta` (float): Probabilidade de Alta Potência (0-1)

**Uso no Python:**
```python
from Integracao_Modelo_Potencia import CarregarModelo_Predicao_Completa

classe, prob_baixa, prob_alta = CarregarModelo_Predicao_Completa(1.80, -0.03, 0.67)
print("Classe prevista:", classe)          # 1
print("Probabilidade Baixa:", prob_baixa)  # 0.008372
print("Probabilidade Alta:", prob_alta)    # 0.991628
```

**Uso no LabVIEW Python Node:**
```
Entradas (DBL):
  - corrente_max: 1.80
  - corrente_min: -0.03
  - corrente_media: 0.67

Saídas:
  - classe (I32): 1
  - prob_baixa (DBL): 0.008372
  - prob_alta (DBL): 0.991628
```

---

## 🔌 Integração com LabVIEW

### Método 1: Python Node (LabVIEW 2018+)

#### Configuração Simples (apenas classe):

```
┌─────────────────────────────────────────────────────────┐
│  Python Node                                             │
│                                                          │
│  Script: Integracao_Modelo_Potencia.py                  │
│  Função: CarregarModelo_Predicao                        │
│                                                          │
│  Entradas (DBL):                                        │
│    ├─ corrente_max                                      │
│    ├─ corrente_min                                      │
│    └─ corrente_media                                    │
│                                                          │
│  Saída (DBL):                                           │
│    └─ classe (0.0 ou 1.0)                              │
└─────────────────────────────────────────────────────────┘
```

#### Configuração Completa (classe + probabilidades):

```
┌─────────────────────────────────────────────────────────┐
│  Python Node                                             │
│                                                          │
│  Script: Integracao_Modelo_Potencia.py                  │
│  Função: CarregarModelo_Predicao_Completa               │
│                                                          │
│  Entradas (DBL):                                        │
│    ├─ corrente_max                                      │
│    ├─ corrente_min                                      │
│    └─ corrente_media                                    │
│                                                          │
│  Saídas:                                                │
│    ├─ classe (I32): 0 ou 1                             │
│    ├─ prob_baixa (DBL): 0-1                            │
│    └─ prob_alta (DBL): 0-1                             │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Exemplos de Teste

### Exemplo 1: Alta Potência

**Entrada:**
- corrente_max = 1.80 A
- corrente_min = -0.03 A
- corrente_media = 0.67 A

**Saída esperada:**
```python
classe = 1 (Alta Potência)
prob_baixa = 0.008372 (0.84%)
prob_alta = 0.991628 (99.16%)
```

### Exemplo 2: Baixa Potência

**Entrada:**
- corrente_max = 1.13 A
- corrente_min = -0.01 A
- corrente_media = 0.47 A

**Saída esperada:**
```python
classe = 0 (Baixa Potência)
prob_baixa = 0.968584 (96.86%)
prob_alta = 0.031416 (3.14%)
```

---

## 🧪 Como Testar

### Teste 1: No Python (antes de integrar com LabVIEW)

Edite o arquivo `Integracao_Modelo_Potencia.py` e descomente as linhas de teste:

```python
# ***** Teste para carregar e fazer predição (apenas classe):
resultado = CarregarModelo_Predicao(1.80, -0.03, 0.67)
print("Classe prevista:", resultado)

# ***** Teste para carregar e fazer predição (completa):
classe, prob_baixa, prob_alta = CarregarModelo_Predicao_Completa(1.80, -0.03, 0.67)
print("Classe prevista:", classe)
print("Probabilidade Baixa:", prob_baixa)
print("Probabilidade Alta:", prob_alta)
```

Execute:
```bash
python3 Integracao_Modelo_Potencia.py
```

### Teste 2: Gerar o modelo (se ainda não existe)

Descomente a linha:
```python
Modelar_Salvar_SVM()
```

Execute:
```bash
python3 Integracao_Modelo_Potencia.py
```

Verifique se o arquivo `modelo_svm_potencia.sav` foi criado.

---

## 📂 Estrutura de Arquivos

```
/Users/enzo/Desktop/ia/Relacoes-Frutiferas/
├── Integracao_Modelo_Potencia.py  ← Arquivo principal
├── modelo_svm_potencia.sav        ← Modelo treinado (gerado)
├── dataset.xls                     ← Dataset de treino
└── INSTRUCOES_LABVIEW.md          ← Este arquivo
```

---

## ⚙️ Requisitos

### Python 3.6 ou superior

```bash
python3 --version
```

### Bibliotecas necessárias:

```bash
pip3 install pandas numpy scikit-learn joblib
```

---

## 🎯 Diferenças em Relação ao Arquivo Original

| Aspecto | Arquivo Original (Iris) | Nosso Arquivo (Potência) |
|---------|------------------------|--------------------------|
| **Dataset** | iris (4 features) | correntes elétricas (3 features + 2 derivadas) |
| **Modelo** | DecisionTreeClassifier | SVM Linear (Pipeline) |
| **Entrada** | 4 valores (A, B, C, D) | 3 valores (max, min, média) |
| **Saída** | Classe (0, 1 ou 2) | Classe (0 ou 1) |
| **Probabilidades** | ❌ Não | ✅ Sim (função completa) |
| **Pré-processamento** | ❌ Não | ✅ StandardScaler |
| **Atributos derivados** | ❌ Não | ✅ Amplitude e Razão |

---

## 🔍 Detalhes Técnicos

### Atributos Derivados Calculados Automaticamente:

O código calcula 2 atributos derivados internamente:

1. **Amplitude de Corrente** = corrente_max - corrente_min
2. **Razão Max/Média** = corrente_max / corrente_media

**Você não precisa calcular isso no LabVIEW!** Apenas forneça as 3 correntes.

### Pipeline do Modelo:

```
Entrada (3 valores) 
    ↓
Cálculo de atributos derivados (+2 valores)
    ↓
StandardScaler (normalização)
    ↓
SVM Linear (classificação)
    ↓
Saída (classe + probabilidades)
```

---

## ✅ Checklist de Integração

- [ ] Python 3.6+ instalado
- [ ] Bibliotecas instaladas (pandas, numpy, sklearn, joblib)
- [ ] Arquivo `modelo_svm_potencia.sav` presente
- [ ] Arquivo `Integracao_Modelo_Potencia.py` presente
- [ ] Teste no Python funcionando
- [ ] Python Node configurado no LabVIEW
- [ ] Teste com valores conhecidos OK
- [ ] Integração com DAQ funcionando

---

## 💡 Dicas para LabVIEW

### 1. Conversão de Classe para Texto

No LabVIEW, após receber a classe (0 ou 1), converta para texto:

```
IF classe == 0 THEN
    nome = "Baixa Potência"
ELSE
    nome = "Alta Potência"
END
```

### 2. Indicador de Confiança

Use `prob_alta` ou `prob_baixa` para criar um indicador visual:

```
confianca = MAX(prob_baixa, prob_alta)

IF confianca > 0.95 THEN
    cor = VERDE (alta confiança)
ELSE IF confianca > 0.80 THEN
    cor = AMARELO (média confiança)
ELSE
    cor = VERMELHO (baixa confiança)
END
```

### 3. Cache do Modelo

Para melhor performance, use o Python Node com estado:
- **Inicialização:** Carregar modelo uma vez
- **Loop:** Reutilizar modelo carregado

Isso evita recarregar o modelo a cada predição.

---

## 📞 Troubleshooting

### Problema: "modelo_svm_potencia.sav não encontrado"

**Solução:** Execute primeiro a função `Modelar_Salvar_SVM()` para gerar o modelo.

### Problema: "ModuleNotFoundError: No module named 'sklearn'"

**Solução:** Instale as bibliotecas:
```bash
pip3 install scikit-learn pandas joblib numpy
```

### Problema: Python Node não encontra o script

**Solução:** Use caminho absoluto:
```
/Users/enzo/Desktop/ia/Relacoes-Frutiferas/Integracao_Modelo_Potencia.py
```

---

**🚀 Pronto para usar no LabVIEW!**

O código segue exatamente o mesmo padrão do arquivo de referência, facilitando a integração.

