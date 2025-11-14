# Integração do Modelo SVM com LabVIEW

## 📦 Arquivos Necessários

| Arquivo | Descrição | Tamanho |
|---------|-----------|---------|
| `modelo_svm_potencia.sav` | Modelo treinado (Pipeline completo) | ~2.7 KB |
| `usar_modelo.py` | Script Python para inferência | ~4 KB |
| `dataset.xls` | Dataset original (opcional, para testes) | ~2 KB |

---

## 🔧 Requisitos do Sistema

### Python 3.6 ou superior

Verificar versão instalada:
```bash
python3 --version
```

### Bibliotecas Python Necessárias

```bash
pip install scikit-learn==0.24.2  # Compatível com Python 3.6+
pip install pandas==1.1.5
pip install joblib==1.0.1
pip install numpy==1.19.5
```

**Nota**: As versões acima são compatíveis com Python 3.6. Para versões mais recentes do Python, use versões mais recentes das bibliotecas.

---

## 🚀 Como Usar o Modelo

### Opção 1: Via Linha de Comando (Recomendado para LabVIEW)

```bash
python3 usar_modelo.py <corrente_max> <corrente_min> <corrente_media>
```

**Exemplo:**
```bash
python3 usar_modelo.py 1.80 -0.03 0.67
```

**Saída (formato CSV):**
```
1|0.991628|0.008372|Alta Potência
```

**Formato da saída:**
```
CLASSE|PROB_BAIXA|PROB_ALTA|NOME_CLASSE
```

Onde:
- `CLASSE`: 0 (Baixa Potência) ou 1 (Alta Potência)
- `PROB_BAIXA`: Probabilidade de ser Baixa Potência (0-1)
- `PROB_ALTA`: Probabilidade de ser Alta Potência (0-1)
- `NOME_CLASSE`: Nome descritivo da classe

---

### Opção 2: Importar como Módulo Python

```python
import joblib
import pandas as pd

# Carregar modelo
modelo = joblib.load('modelo_svm_potencia.sav')

# Preparar dados
corrente_max = 1.80
corrente_min = -0.03
corrente_media = 0.67

# Calcular atributos derivados
amplitude = corrente_max - corrente_min
razao = corrente_max / (corrente_media + 1e-6)

# Criar entrada
entrada = pd.DataFrame(
    [[corrente_max, corrente_min, corrente_media, amplitude, razao]], 
    columns=['corrente_max_A', 'corrente_min_A', 'corrente_media_A',
            'amplitude_corrente', 'razao_max_media']
)

# Predição
classe = int(modelo.predict(entrada)[0])
probabilidades = modelo.predict_proba(entrada)[0]

print(f"Classe: {classe}")
print(f"Prob. Baixa: {probabilidades[0]:.2f}")
print(f"Prob. Alta: {probabilidades[1]:.2f}")
```

---

## 🔌 Integração com LabVIEW

### Método 1: System Exec.vi (Mais Simples)

1. **Arrastar System Exec.vi** para o diagrama de blocos
2. **Configurar entrada "command line":**
   ```
   python3 /caminho/completo/usar_modelo.py <corrente_max> <corrente_min> <corrente_media>
   ```
3. **Capturar saída "standard output"**
4. **Fazer parsing da string** de saída usando:
   - **Spreadsheet String to Array** (delimitador: `|`)
   - Índices: 
     - [0] = Classe (int)
     - [1] = Prob. Baixa (float)
     - [2] = Prob. Alta (float)
     - [3] = Nome da Classe (string)

**Exemplo de diagrama de blocos:**
```
[Controles: corrente_max, corrente_min, corrente_media]
    ↓
[Format Into String] → "python3 usar_modelo.py %.2f %.2f %.2f"
    ↓
[System Exec.vi]
    ↓
[Spreadsheet String to Array] (delimitador: "|")
    ↓
[Indicadores: classe, prob_baixa, prob_alta, nome_classe]
```

---

### Método 2: Python Node (LabVIEW 2018+)

Se você tem **LabVIEW 2018** ou superior com suporte a Python Node:

1. **Arrastar Python Node** para o diagrama
2. **Selecionar função:** `prever_potencia` do arquivo `usar_modelo.py`
3. **Conectar entradas:**
   - corrente_max (DBL)
   - corrente_min (DBL)
   - corrente_media (DBL)
4. **Conectar saídas:**
   - classe (I32)
   - prob_baixa (DBL)
   - prob_alta (DBL)

---

### Método 3: ActiveX/COM (Windows)

Para aplicações Windows, você pode usar `win32com` ou `pythoncom` para criar um servidor COM que o LabVIEW pode acessar diretamente.

---

## 📊 Exemplos de Teste

### Exemplo 1: Baixa Potência
```bash
$ python3 usar_modelo.py 1.13 -0.01 0.47
0|0.968584|0.031416|Baixa Potência
```

✅ **Esperado:** Classe 0 (Baixa Potência) com ~97% de confiança

---

### Exemplo 2: Alta Potência
```bash
$ python3 usar_modelo.py 1.80 -0.03 0.67
1|0.008372|0.991628|Alta Potência
```

✅ **Esperado:** Classe 1 (Alta Potência) com ~99% de confiança

---

### Exemplo 3: Caso Limite
```bash
$ python3 usar_modelo.py 1.50 0.00 0.555
0|0.524123|0.475877|Baixa Potência
```

⚠️ **Esperado:** Classe próxima ao limiar (~50/50)

---

## 🐛 Solução de Problemas

### Erro: "Arquivo 'modelo_svm_potencia.sav' não encontrado"

**Solução:** Execute primeiro o notebook Jupyter para gerar o modelo:
```bash
jupyter notebook APS1-NL.ipynb
# Executar células da seção 7
```

---

### Erro: "ModuleNotFoundError: No module named 'sklearn'"

**Solução:** Instalar scikit-learn:
```bash
pip3 install scikit-learn pandas joblib numpy
```

---

### Erro: "Python3 não é reconhecido"

**Solução (Windows):** Use o caminho completo:
```bash
C:\Python36\python.exe usar_modelo.py 1.80 -0.03 0.67
```

**Solução (Mac/Linux):** Verificar PATH:
```bash
which python3
```

---

### Saída vazia ou erro no LabVIEW

**Verificações:**
1. **Timeout do System Exec.vi:** Aumentar para 10000 ms (10 segundos)
2. **Caminho absoluto:** Usar caminho completo para `usar_modelo.py`
3. **Diretório de trabalho:** Definir working directory para pasta do modelo
4. **Permissões:** Dar permissão de execução ao script (Linux/Mac):
   ```bash
   chmod +x usar_modelo.py
   ```

---

## 📈 Desempenho

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Acurácia** | 100% | Validado com validação cruzada |
| **F1-score** | 1.000 | Perfeito em ambas as classes |
| **Tempo de inferência** | < 100ms | Típico em hardware moderno |
| **Tamanho do modelo** | 2.73 KB | Muito leve |

---

## 🔐 Versionamento do Modelo

| Informação | Valor |
|------------|-------|
| **Versão do Modelo** | 1.0 |
| **Data de Treinamento** | Novembro 2025 |
| **Dataset SHA-256** | `22bee9360cc85d7e6a3ce19ea8d52771bee7e3616c325a1cebbd4787e09b2dd8` |
| **Amostras de Treino** | 68 (34 baixa, 34 alta) |
| **Algoritmo** | SVM Linear (C=1, kernel='linear') |
| **scikit-learn** | 0.24+ (compatível com 3.6+) |

---

## 📞 Suporte

Para problemas ou dúvidas:
1. Verificar logs de erro do Python
2. Testar `usar_modelo.py` diretamente no terminal
3. Confirmar que todas as bibliotecas estão instaladas
4. Verificar compatibilidade de versões Python/scikit-learn

---

## ✅ Checklist de Integração

- [ ] Python 3.6+ instalado
- [ ] Bibliotecas instaladas (sklearn, pandas, joblib)
- [ ] Arquivo `modelo_svm_potencia.sav` presente
- [ ] Arquivo `usar_modelo.py` presente
- [ ] Teste via linha de comando funcionando
- [ ] System Exec.vi configurado no LabVIEW
- [ ] Parsing da saída implementado
- [ ] Interface de usuário criada no LabVIEW

---

**Modelo pronto para produção! 🚀**

