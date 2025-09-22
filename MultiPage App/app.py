import streamlit as st

st.set_page_config(layout="wide", page_title="Dashboard JII2025")

# ============================
# Título
# ============================
st.title("📈 Dashboard de la Jornada de Ingeniería Industrial 2025")

# ============================
# Introducción
# ============================
st.subheader("Introducción")
st.markdown("""
Este panel de simulación permite **analizar y cuantificar** el impacto de la asignación de recursos en los cronogramas de proyectos de construcción. 
La gestión eficiente de **materiales, mano de obra y presupuesto** es crítica para minimizar retrasos y asegurar la rentabilidad.

**Propósito:** entregar una herramienta interactiva para que los gestores de proyectos puedan **modelar escenarios hipotéticos**, 
comprender las sensibilidades del proyecto y tomar decisiones informadas para optimizar la asignación de recursos.
""")

st.divider()

# ============================
# ¿Qué es este simulador?
# ============================
st.subheader("¿Qué es este simulador?")
st.markdown("""
Es una herramienta que aplica un **modelo matemático determinista** para calcular cómo las variaciones en la disponibilidad de recursos 
afectan los retrasos de un portafolio de proyectos.  

Permite responder preguntas como:
- ¿Cuál es el impacto en el **retraso total** si sufrimos un recorte presupuestario del 15%?
- ¿Podemos compensar una **escasez de mano de obra** aumentando la inversión en materiales?
- ¿Qué **combinación de recursos** minimiza los retrasos promedio en todos los proyectos?
- ¿Cómo cambia la **eficiencia temporal** (proyectos terminados a tiempo) al variar los factores?
""")

st.divider()

# ============================
# Modelo de Simulación
# ============================
st.subheader("Modelo de Simulación")

st.markdown("""
##### Controles y Cálculo del Retraso Simulado

- **Factores de Recursos:** Materiales, Mano de Obra y Presupuesto, representados como fracciones del 100% de disponibilidad.
- **Relación Lineal:** El retraso simulado aumenta linealmente si los recursos se reducen, ponderando cada recurso según su importancia.
""")

st.markdown("**Fórmula del Modelo:**")
st.latex(r"""
R_{\text{simulado}} = R_{\text{original}} + \sum_{i=1}^{3} w_i \cdot \max(0, 1 - f_i) \cdot R_{\text{original}}
""")

st.markdown("""
Donde:
- $R_{\t{simulado}}$ = Retraso simulado (días)
- $R_{\t{original}}$ = Retraso original (días)
- $w_i$ = Peso del recurso $i$ (Materiales, Mano de Obra, Presupuesto)
- $f_i$ = Factor del recurso $i$ (0.5 a 1.5, donde 1.0 = 100%)
- $\max(0, 1 - f_i)$ = Penaliza solo déficit de recursos ($f_i < 1$)
""")

st.markdown("**Pesos de Impacto por Defecto:**")
st.latex(r"""
\begin{align}
w_{\text{materiales}} &= 0.4 \\
w_{\text{mano\_obra}} &= 0.5 \\
w_{\text{presupuesto}} &= 0.3
\end{align}
""")

# ============================
# Métricas Clave
# ============================
st.subheader("Métricas Clave del Simulador")

st.markdown("Estas métricas permiten evaluar el impacto de los ajustes de recursos sobre los proyectos:")

# Retraso Total Simulado
st.markdown("**Retraso Total Simulado:**")
st.latex(r"""
RT = \sum_{j=1}^{n} R_{\text{simulado}, j}
""")
st.markdown("donde $n$ es el número de proyectos y $R_{\t{simulado}, j}$ es el retraso simulado del proyecto $j$.")

# Retraso Promedio Simulado
st.markdown("**Retraso Promedio Simulado:**")
st.latex(r"""
RP = \frac{1}{n} \sum_{j=1}^{n} R_{\text{simulado}, j}
""")
st.markdown("Promedio de los retrasos simulados de todos los proyectos.")

# Eficiencia Temporal Simulada
st.markdown("**Eficiencia Temporal Simulada:**")
st.latex(r"""
ET = \frac{\text{Número de proyectos con } R_{\text{simulado}} \leq 0}{n} \times 100\%
""")
st.markdown("Porcentaje de proyectos que se completan a tiempo (retraso ≤ 0).")

# Índice de Impacto de Recursos
st.markdown("**Índice de Impacto de Recursos:**")
st.latex(r"""
IIR = \frac{RT_{\text{simulado}} - RT_{\text{original}}}{RT_{\text{original}}} \times 100\%
""")
st.markdown("Indica el cambio porcentual en el retraso total con respecto a la línea base.")

st.divider()

# ============================
# Modelo de Optimización Lineal
# ============================
st.subheader("Modelo de Optimización Lineal")

st.markdown("""
El objetivo de la **optimización lineal** es encontrar la **mejor combinación de recursos** que minimice el retraso total de todos los proyectos, respetando restricciones de disponibilidad.

### Función Objetivo:
$$
\t{Minimizar } Z = 0.1 \cdot (100 - F_{\text{mat}}) + 0.1 \cdot (100 - F_{\text{mo}}) + 0.05 \cdot (100 - F_{\text{pres}})
$$

### Restricciones:
$$
0 \leq F_{\t{mat}} \leq \t{Max Materiales}, \quad
0 \leq F_{\t{mo}} \leq \t{Max Mano de Obra}, \quad
0 \leq F_{\t{pres}} \leq \t{Max Presupuesto}
$$

- $F_{\t{mat}}, F_{\t{mo}}, F_{\t{pres}}$ = factores óptimos de cada recurso que minimizan el retraso.
- La optimización considera la relación lineal entre déficit de recursos y aumento de retrasos, usando los mismos pesos que el simulador.

### Justificación:
Este modelo permite a los gestores identificar dónde asignar recursos adicionales o redistribuirlos para **maximizar eficiencia y reducir retrasos**.
""")

st.divider()

# ============================
# Integración Simulador ↔ Optimización
# ============================
st.subheader("Cómo trabajan juntos el Simulador y el Modelo de Optimización")
st.markdown("""
El **simulador de escenarios** y el **modelo de optimización lineal** se complementan:

1. **Simulador:**  
   - Explora escenarios hipotéticos ajustando los factores de recursos.
   - Calcula el retraso simulado por proyecto con la fórmula $R_{\t{simulado}}$.

2. **Optimización Lineal:**  
   - Analiza los escenarios simulados y determina la asignación óptima $F_{\t{mat}}, F_{\t{mo}}, F_{\t{pres}}$.
   - Minimiza la función objetivo $Z$, respetando las restricciones de cada recurso.

**Flujo de trabajo:**
- Los datos de los proyectos ingresan al simulador.
- El simulador calcula los retrasos simulados para distintos escenarios.
- La optimización lineal encuentra la mejor combinación de recursos.
- Los resultados permiten a los gestores tomar decisiones informadas para **minimizar retrasos y maximizar eficiencia**.
""")

st.divider()

# ============================
# Guía de uso
# ============================
st.subheader("Guía de uso")
st.markdown("""
1. Analiza la línea base con todos los factores al 100%.
2. Explora escenarios hipotéticos para observar los impactos.
3. Usa la optimización lineal para determinar la mejor combinación de recursos.
4. Justifica solicitudes de presupuesto adicional con base en los resultados cuantitativos.
""")
