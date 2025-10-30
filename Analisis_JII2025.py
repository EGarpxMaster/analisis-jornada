
import streamlit as st

st.set_page_config(layout="wide", page_title="Dashboard JII2025")

# ============================
# Documentación académica
# ============================
st.markdown("""
# Dashboard de la Jornada de Ingeniería Industrial 2025

## Descripción Académica

Este dashboard constituye una herramienta de análisis y evaluación orientada al estudio de datos del evento académico Jornada de Ingeniería Industrial 2025. Su diseño responde a la necesidad de proporcionar a los organizadores y responsables una plataforma interactiva para la evaluación cuantitativa de la participación, análisis de encuestas de satisfacción y procesamiento de retroalimentación cualitativa mediante técnicas de procesamiento de lenguaje natural.

### Propósito
El objetivo principal es facilitar la toma de decisiones basada en datos para mejorar la organización de eventos académicos futuros. El dashboard permite visualizar patrones de participación, analizar la satisfacción de los asistentes mediante encuestas cuantitativas, e interpretar comentarios y sugerencias de texto libre usando análisis de sentimientos.

### Alcance
La aplicación integra:
- Visualización en tiempo real de datos almacenados en Supabase (base de datos PostgreSQL en la nube).
- Tablas de datos de participantes, inscripciones a actividades, equipos de concurso y respuestas de encuesta.
- Dashboard con métricas clave de participación e indicadores de desempeño del evento.
- Análisis cuantitativo de encuestas con gráficos de distribución, promedios y comparativas por categoría.
- Análisis de sentimientos básico de respuestas de texto largo usando procesamiento de lenguaje natural.
- Exportación de datos en formato CSV para análisis externos.

### Fundamentación
El desarrollo se fundamenta en principios de análisis de datos, visualización interactiva y procesamiento de lenguaje natural. La arquitectura utiliza Streamlit como framework de presentación, Pandas para manipulación de datos, Plotly para visualizaciones interactivas, y técnicas básicas de NLP para clasificación de sentimientos. La conexión a Supabase garantiza actualización en tiempo real y escalabilidad.

### Metodología de Análisis
**Análisis Cuantitativo:**
- Estadísticas descriptivas (promedios, medianas, desviaciones estándar)
- Distribuciones de frecuencia
- Comparativas por categorías y segmentos
- Visualizaciones interactivas (gráficos de barras, tortas, líneas)

**Análisis Cualitativo:**
- Análisis de frecuencia de palabras clave
- Clasificación de sentimientos basada en léxico
- Exploración de respuestas de texto largo
- Identificación de patrones temáticos

### Aplicación
Este dashboard es adecuado para entornos académicos donde se requiera evaluar la efectividad de eventos, analizar la satisfacción de participantes y obtener insights accionables para mejoras continuas. Su estructura modular permite adaptación a otros tipos de eventos y la integración de modelos de análisis más avanzados.

### Estructura del Dashboard
1. **Tablas de Datos:** Consulta directa de todas las tablas de la base de datos
2. **Dashboard Principal:** Visualizaciones y métricas clave del evento
3. **Análisis de Encuesta:** Evaluación cuantitativa de respuestas de calificación (escala 1-5)
4. **Análisis de Sentimientos:** Procesamiento de respuestas de texto libre
""")
