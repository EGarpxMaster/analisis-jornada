
import streamlit as st

st.set_page_config(layout="wide", page_title="Dashboard JII2025")

# ============================
# Documentación académica
# ============================
st.markdown("""
# Dashboard de la Jornada de Ingeniería Industrial 2025

## Descripción Académica

Este dashboard constituye una herramienta de análisis y simulación orientada a la gestión de proyectos en el contexto de la Jornada de Ingeniería Industrial 2025. Su diseño responde a la necesidad de proporcionar a los responsables de la toma de decisiones una plataforma interactiva para la evaluación cuantitativa de escenarios, el modelado de sensibilidades y la optimización de recursos.

### Propósito
El objetivo principal es facilitar el análisis de cómo las variaciones en la disponibilidad de recursos (materiales, mano de obra y presupuesto) impactan en los retrasos de un portafolio de proyectos. El dashboard permite simular escenarios hipotéticos, calcular métricas clave de desempeño y aplicar modelos matemáticos para la optimización de la asignación de recursos.

### Alcance
La aplicación integra:
- Un simulador determinista basado en relaciones lineales entre déficit de recursos y aumento de retrasos.
- Métricas agregadas para evaluar el impacto global y promedio sobre los proyectos.
- Un modelo de optimización lineal que identifica la combinación óptima de recursos para minimizar el retraso total, sujeto a restricciones operativas.
- Visualización y justificación cuantitativa de decisiones de gestión.

### Fundamentación
El desarrollo se fundamenta en principios de gestión de proyectos, teoría de optimización y análisis de sensibilidad. El modelo matemático implementado penaliza únicamente los déficits de recursos, ponderando su impacto según parámetros definidos por el usuario o por la literatura especializada. La optimización lineal emplea una función objetivo que busca minimizar el retraso total, respetando las restricciones de disponibilidad de cada recurso.

### Aplicación
Este dashboard es adecuado para entornos académicos y profesionales donde se requiera justificar decisiones de asignación de recursos, analizar escenarios de contingencia y optimizar el desempeño temporal de proyectos. Su estructura modular permite la extensión a otros contextos y la integración de nuevos modelos analíticos.
""")
