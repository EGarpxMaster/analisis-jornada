# Configuración de Análisis de Sentimientos con TextBlob

Este documento explica cómo configurar y usar TextBlob para el análisis de sentimientos avanzado en el dashboard.

## 📦 Instalación

### 1. Instalar dependencias

Ejecuta el siguiente comando para instalar TextBlob:

```bash
pip install textblob
```

### 2. Descargar corpus de TextBlob

Después de instalar, descarga los datos necesarios para el análisis de lenguaje natural:

```bash
python -m textblob.download_corpora
```

Este comando descargará los modelos de NLP necesarios (~500MB).

## 🔧 Configuración en Streamlit Cloud

Si despliegas en Streamlit Cloud, agrega las siguientes líneas al archivo `packages.txt` (créalo si no existe):

```
python3-nltk
```

Y en tu `requirements.txt` ya está incluida:
```
textblob>=0.17.0
```

**Nota**: TextBlob funciona en cualquier idioma, aunque está optimizado para inglés. Para español, el análisis de sentimientos funciona adecuadamente con el corpus estándar.

## 📊 Funcionalidades

El análisis de sentimientos con TextBlob proporciona:

### 1. **Polaridad** (-1 a +1)
- **-1.0 a -0.1**: Sentimiento Negativo
- **-0.1 a +0.1**: Sentimiento Neutral
- **+0.1 a +1.0**: Sentimiento Positivo

### 2. **Subjetividad** (0 a 1)
- **0.0**: Texto completamente objetivo (hechos)
- **1.0**: Texto completamente subjetivo (opiniones)

## 📈 Visualizaciones Disponibles

1. **Distribución de Sentimientos**: Gráfico de pastel con porcentajes
2. **Polaridad vs Subjetividad**: Scatter plot interactivo
3. **Histograma de Polaridad**: Distribución de valores de polaridad
4. **Histograma de Subjetividad**: Distribución de valores de subjetividad
5. **Ejemplos por Sentimiento**: Respuestas ordenadas por polaridad

## 🔒 Privacidad

Todas las respuestas de la encuesta se muestran de forma **anónima**. Los participantes se identifican como:
- `Participante_001`
- `Participante_002`
- etc.

No se muestra información personal como emails o nombres completos.

## 🚀 Uso

1. Ve a la página **"4_Analisis_Sentimientos"**
2. Selecciona una pregunta de texto largo
3. El sistema analizará automáticamente todas las respuestas
4. Visualiza las métricas y gráficos generados

## 🐛 Troubleshooting

### Error: "TextBlob no está instalado"

**Solución**: 
```bash
pip install textblob
python -m textblob.download_corpora
```

### Error: "LookupError: Resource punkt not found"

**Solución**:
```bash
python -m textblob.download_corpora
```

O en Python:
```python
import nltk
nltk.download('punkt')
nltk.download('brown')
nltk.download('punkt_tab')
```

### Análisis lento

TextBlob procesa cada texto individualmente. Para grandes volúmenes:
- Los resultados se cachean con `@st.cache_data`
- El análisis solo se ejecuta una vez por sesión
- Considera usar análisis batch para miles de respuestas

## 📚 Recursos Adicionales

- [Documentación TextBlob](https://textblob.readthedocs.io/)
- [Tutorial de Sentiment Analysis](https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis)
- [TextBlob para Español](https://github.com/s2t2/textblob-es)

## 🔄 Alternativas Avanzadas

Para análisis más sofisticados, considera:

1. **spaCy con modelos en español**
   ```bash
   pip install spacy
   python -m spacy download es_core_news_sm
   ```

2. **Transformers (BERT, RoBERTa)**
   ```bash
   pip install transformers
   ```
   Usa modelos pre-entrenados como `dccuchile/bert-base-spanish-wwm-cased`

3. **VADER (Valence Aware Dictionary)**
   ```bash
   pip install vaderSentiment
   ```

---

**Dashboard JII 2025** | Análisis de Sentimientos con NLP Avanzado
