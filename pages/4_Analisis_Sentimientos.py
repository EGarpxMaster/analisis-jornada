"""
Análisis de Sentimientos - Jornada de Ingeniería Industrial 2025
Análisis de texto de respuestas abiertas usando procesamiento de lenguaje natural
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import sys
from pathlib import Path

# Agregar el directorio raíz al path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.supabase_client import obtener_respuestas_encuesta
from utils.preguntas_encuesta import PREGUNTAS_TEXTO_LARGO, obtener_pregunta_por_id

# Importar TextBlob para análisis de sentimientos avanzado
try:
    from textblob import TextBlob
    TEXTBLOB_DISPONIBLE = True
except ImportError:
    TEXTBLOB_DISPONIBLE = False
    st.warning("⚠️ TextBlob no está instalado. Ejecuta: `pip install textblob textblob-es` para análisis avanzado.")

st.set_page_config(
    page_title="Análisis de Sentimientos JII 2025",
    page_icon="💬",
    layout="wide"
)

st.title("Análisis de Sentimientos - Jornada de Ingeniería Industrial 2025")
st.markdown("Análisis de respuestas de texto largo mediante procesamiento de lenguaje natural")

# Cargar todas las respuestas de encuesta (ANONIMIZADAS)
with st.spinner("Cargando respuestas de encuesta..."):
    df_respuestas = obtener_respuestas_encuesta(anonimizar=True)

if df_respuestas.empty:
    st.warning("No hay respuestas de encuesta disponibles")
    st.stop()

# Filtrar solo preguntas de texto largo
ids_texto_largo = [p['id'] for p in PREGUNTAS_TEXTO_LARGO]
df_texto = df_respuestas[df_respuestas['pregunta_id'].isin(ids_texto_largo)].copy()

if df_texto.empty:
    st.warning("No hay respuestas de texto largo disponibles")
    st.stop()

# Limpiar respuestas vacías
df_texto = df_texto[df_texto['respuesta'].notna()]
df_texto = df_texto[df_texto['respuesta'].str.strip() != '']

# Estadísticas generales
st.subheader("Estadísticas Generales")
col1, col2, col3, col4 = st.columns(4)

total_respuestas_texto = len(df_texto)
participantes_texto = df_texto['participante_anonimo'].nunique() if 'participante_anonimo' in df_texto.columns else 0
preguntas_texto = df_texto['pregunta_id'].nunique()
promedio_longitud = df_texto['respuesta'].str.len().mean()

col1.metric("Total de Respuestas de Texto", total_respuestas_texto)
col2.metric("Participantes Únicos (Anónimos)", participantes_texto)
col3.metric("Preguntas con Texto", preguntas_texto)
col4.metric("Longitud Promedio", f"{promedio_longitud:.0f} caracteres")

st.markdown("---")

# Tabs para diferentes análisis
tab1, tab2, tab3 = st.tabs([
    "Exploración de Respuestas",
    "Análisis de Frecuencia de Palabras", 
    "Análisis de Sentimientos Básico"
])

with tab1:
    st.markdown("### Exploración de Respuestas por Pregunta")
    
    # Selector de pregunta
    preguntas_opciones = {
        f"{p['id']}: {p['texto'][:80]}...": p['id'] 
        for p in PREGUNTAS_TEXTO_LARGO
    }
    
    pregunta_seleccionada = st.selectbox(
        "Selecciona una pregunta para analizar",
        options=list(preguntas_opciones.keys())
    )
    
    pregunta_id = preguntas_opciones[pregunta_seleccionada]
    pregunta_info = obtener_pregunta_por_id(pregunta_id)
    
    # Filtrar respuestas de la pregunta seleccionada
    df_pregunta = df_texto[df_texto['pregunta_id'] == pregunta_id]
    
    if not df_pregunta.empty:
        st.markdown(f"**Pregunta:** {pregunta_info['texto']}")
        st.markdown(f"**Total de respuestas:** {len(df_pregunta)}")
        
        # Mostrar todas las respuestas en un expander (ANÓNIMAS)
        with st.expander("Ver todas las respuestas", expanded=False):
            for idx, row in df_pregunta.iterrows():
                participante_id = row.get('participante_anonimo', 'Participante Anónimo')
                st.markdown(f"**{participante_id}**")
                st.write(row['respuesta'])
                st.markdown("---")
        
        # Estadísticas de longitud
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Estadísticas de Longitud")
            longitudes = df_pregunta['respuesta'].str.len()
            st.metric("Mínimo", f"{longitudes.min()} caracteres")
            st.metric("Máximo", f"{longitudes.max()} caracteres")
            st.metric("Promedio", f"{longitudes.mean():.0f} caracteres")
            st.metric("Mediana", f"{longitudes.median():.0f} caracteres")
        
        with col2:
            # Histograma de longitudes
            fig_long = px.histogram(
                longitudes,
                nbins=20,
                title="Distribución de Longitud de Respuestas",
                labels={'value': 'Longitud (caracteres)', 'count': 'Frecuencia'}
            )
            st.plotly_chart(fig_long, use_container_width=True)
    else:
        st.info("No hay respuestas para esta pregunta")

with tab2:
    st.markdown("### Análisis de Frecuencia de Palabras")
    
    # Selector de pregunta
    pregunta_seleccionada_freq = st.selectbox(
        "Selecciona una pregunta para análisis de frecuencia",
        options=list(preguntas_opciones.keys()),
        key="freq_selector"
    )
    
    pregunta_id_freq = preguntas_opciones[pregunta_seleccionada_freq]
    df_pregunta_freq = df_texto[df_texto['pregunta_id'] == pregunta_id_freq]
    
    if not df_pregunta_freq.empty:
        # Combinar todas las respuestas
        texto_completo = ' '.join(df_pregunta_freq['respuesta'].tolist())
        
        # Palabras de parada en español (básicas)
        stopwords_es = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'haber',
            'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'lo', 'todo',
            'pero', 'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir', 'otro', 'ese',
            'si', 'me', 'ya', 'ver', 'porque', 'dar', 'cuando', 'él', 'muy', 'sin',
            'vez', 'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo', 'yo',
            'también', 'hasta', 'año', 'dos', 'querer', 'entre', 'así', 'primero',
            'desde', 'grande', 'eso', 'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella',
            'una', 'las', 'los', 'del', 'al', 'es', 'son', 'fue', 'han', 'era', 'está',
            'están', 'fue', 'fueron', 'sido', 'tiene', 'tienen', 'había', 'hay', 'puede',
            'pueden', 'esta', 'estos', 'estas', 'este', 'esos', 'esas', 'ese', 'esa',
            'mas', 'aunque', 'solo', 'sólo', 'fue', 'etc'
        }
        
        # Procesar texto
        palabras = texto_completo.lower().split()
        palabras = [p.strip('.,;:!?¡¿()[]{}"\'-') for p in palabras]
        palabras = [p for p in palabras if len(p) > 3 and p not in stopwords_es]
        
        # Contar frecuencias
        frecuencias = Counter(palabras)
        top_n = st.slider("Número de palabras más frecuentes", 10, 50, 20)
        top_palabras = frecuencias.most_common(top_n)
        
        if top_palabras:
            df_freq = pd.DataFrame(top_palabras, columns=['Palabra', 'Frecuencia'])
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Gráfico de barras
                fig_freq = px.bar(
                    df_freq,
                    x='Frecuencia',
                    y='Palabra',
                    orientation='h',
                    title=f'Top {top_n} Palabras Más Frecuentes',
                    text='Frecuencia'
                )
                fig_freq.update_traces(textposition='outside')
                fig_freq.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_freq, use_container_width=True)
            
            with col2:
                st.markdown("#### Tabla de Frecuencias")
                st.dataframe(df_freq, use_container_width=True, hide_index=True)
        else:
            st.info("No hay suficientes palabras para analizar")
    else:
        st.info("No hay respuestas para esta pregunta")

with tab3:
    st.markdown("### Análisis de Sentimientos Avanzado con TextBlob")
    
    if not TEXTBLOB_DISPONIBLE:
        st.error("""
        ❌ **TextBlob no está instalado.**
        
        Para habilitar el análisis de sentimientos avanzado, ejecuta:
        ```
        pip install textblob textblob-es
        python -m textblob.download_corpora
        ```
        """)
        st.stop()
    
    st.info("""
    **Análisis con TextBlob:** Utiliza procesamiento de lenguaje natural para analizar:
    - **Polaridad:** Mide el sentimiento (negativo a positivo) en escala de -1 a +1
    - **Subjetividad:** Mide qué tan objetivo/subjetivo es el texto (0 = objetivo, 1 = subjetivo)
    """)
    
    # Selector de pregunta
    pregunta_seleccionada_sent = st.selectbox(
        "Selecciona una pregunta para análisis de sentimientos",
        options=list(preguntas_opciones.keys()),
        key="sent_selector"
    )
    
    pregunta_id_sent = preguntas_opciones[pregunta_seleccionada_sent]
    df_pregunta_sent = df_texto[df_texto['pregunta_id'] == pregunta_id_sent].copy()
    
    if not df_pregunta_sent.empty:
        # Función para analizar sentimiento con TextBlob
        @st.cache_data
        def analizar_sentimiento_textblob(texto):
            """Analiza el sentimiento usando TextBlob"""
            try:
                blob = TextBlob(texto)
                # Traducir al inglés para mejor precisión (TextBlob funciona mejor en inglés)
                # pero primero intentamos directamente en español
                polaridad = blob.sentiment.polarity
                subjetividad = blob.sentiment.subjectivity
                
                # Clasificar según polaridad
                if polaridad > 0.1:
                    sentimiento = 'Positivo'
                elif polaridad < -0.1:
                    sentimiento = 'Negativo'
                else:
                    sentimiento = 'Neutral'
                
                return sentimiento, polaridad, subjetividad
            except Exception as e:
                return 'Neutral', 0.0, 0.5
        
        # Analizar todas las respuestas
        with st.spinner("Analizando sentimientos con TextBlob..."):
            resultados = df_pregunta_sent['respuesta'].apply(analizar_sentimiento_textblob)
            df_pregunta_sent['sentimiento'] = resultados.apply(lambda x: x[0])
            df_pregunta_sent['polaridad'] = resultados.apply(lambda x: x[1])
            df_pregunta_sent['subjetividad'] = resultados.apply(lambda x: x[2])
        
        # Estadísticas y visualizaciones
        st.markdown("---")
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        promedio_polaridad = df_pregunta_sent['polaridad'].mean()
        promedio_subjetividad = df_pregunta_sent['subjetividad'].mean()
        conteo_sentimientos = df_pregunta_sent['sentimiento'].value_counts()
        
        col1.metric("Polaridad Promedio", f"{promedio_polaridad:.3f}", 
                   help="De -1 (negativo) a +1 (positivo)")
        col2.metric("Subjetividad Promedio", f"{promedio_subjetividad:.3f}",
                   help="De 0 (objetivo) a 1 (subjetivo)")
        col3.metric("Respuestas Positivas", 
                   conteo_sentimientos.get('Positivo', 0),
                   f"{conteo_sentimientos.get('Positivo', 0) / len(df_pregunta_sent) * 100:.1f}%")
        col4.metric("Respuestas Negativas", 
                   conteo_sentimientos.get('Negativo', 0),
                   f"{conteo_sentimientos.get('Negativo', 0) / len(df_pregunta_sent) * 100:.1f}%")
        
        st.markdown("---")
        
        # Visualizaciones en dos columnas
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de torta - Distribución de sentimientos
            fig_sent = px.pie(
                values=conteo_sentimientos.values,
                names=conteo_sentimientos.index,
                title='Distribución de Sentimientos',
                color=conteo_sentimientos.index,
                color_discrete_map={
                    'Positivo': '#28a745',
                    'Neutral': '#ffc107',
                    'Negativo': '#dc3545'
                },
                hole=0.4
            )
            st.plotly_chart(fig_sent, use_container_width=True)
            
            # Histograma de polaridad
            fig_pol = px.histogram(
                df_pregunta_sent,
                x='polaridad',
                nbins=20,
                title='Distribución de Polaridad',
                labels={'polaridad': 'Polaridad', 'count': 'Frecuencia'},
                color_discrete_sequence=['steelblue']
            )
            fig_pol.add_vline(x=0, line_dash="dash", line_color="red", 
                            annotation_text="Neutral")
            st.plotly_chart(fig_pol, use_container_width=True)
        
        with col2:
            # Scatter plot: Polaridad vs Subjetividad
            fig_scatter = px.scatter(
                df_pregunta_sent,
                x='polaridad',
                y='subjetividad',
                color='sentimiento',
                title='Polaridad vs Subjetividad',
                labels={'polaridad': 'Polaridad', 'subjetividad': 'Subjetividad'},
                color_discrete_map={
                    'Positivo': '#28a745',
                    'Neutral': '#ffc107',
                    'Negativo': '#dc3545'
                },
                hover_data=['respuesta']
            )
            fig_scatter.add_hline(y=0.5, line_dash="dash", line_color="gray")
            fig_scatter.add_vline(x=0, line_dash="dash", line_color="gray")
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Histograma de subjetividad
            fig_subj = px.histogram(
                df_pregunta_sent,
                x='subjetividad',
                nbins=20,
                title='Distribución de Subjetividad',
                labels={'subjetividad': 'Subjetividad', 'count': 'Frecuencia'},
                color_discrete_sequence=['coral']
            )
            fig_subj.add_vline(x=0.5, line_dash="dash", line_color="red", 
                             annotation_text="Media")
            st.plotly_chart(fig_subj, use_container_width=True)
        
        # Mostrar ejemplos por sentimiento (ANÓNIMAS)
        st.markdown("---")
        st.markdown("#### Ejemplos de Respuestas por Sentimiento (Anónimas)")
        
        sent_tabs = st.tabs(["Positivo", "Neutral", "Negativo"])
        
        for idx, (tab, sentimiento) in enumerate(zip(sent_tabs, ['Positivo', 'Neutral', 'Negativo'])):
            with tab:
                respuestas_sent = df_pregunta_sent[df_pregunta_sent['sentimiento'] == sentimiento]
                if not respuestas_sent.empty:
                    num_mostrar = min(5, len(respuestas_sent))
                    st.markdown(f"**Mostrando {num_mostrar} de {len(respuestas_sent)} respuestas**")
                    
                    # Ordenar por polaridad para mostrar ejemplos más representativos
                    if sentimiento == 'Positivo':
                        respuestas_sent = respuestas_sent.sort_values('polaridad', ascending=False)
                    elif sentimiento == 'Negativo':
                        respuestas_sent = respuestas_sent.sort_values('polaridad', ascending=True)
                    
                    for i, (_, row) in enumerate(respuestas_sent.head(num_mostrar).iterrows(), 1):
                        participante_id = row.get('participante_anonimo', f'Participante Anónimo {i}')
                        with st.expander(f"{participante_id} - Polaridad: {row['polaridad']:.3f} | Subjetividad: {row['subjetividad']:.3f}"):
                            st.write(row['respuesta'])
                else:
                    st.info(f"No hay respuestas clasificadas como {sentimiento}")
    else:
        st.info("No hay respuestas para esta pregunta")

# Descargar datos
st.markdown("---")
st.subheader("Exportar Datos")

if not df_texto.empty:
    csv_texto = df_texto.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar Respuestas de Texto (CSV)",
        data=csv_texto,
        file_name="respuestas_texto_jii2025.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("Dashboard JII 2025 - Análisis de Sentimientos")
st.caption("⚠️ Nota: El análisis de sentimientos es básico. Para análisis avanzados, considere integrar modelos de NLP como spaCy o transformers.")
