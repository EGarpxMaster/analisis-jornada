"""
Análisis de Sentimientos - Jornada de Ingeniería Industrial 2025
Análisis de texto de respuestas abiertas usando procesamiento de lenguaje natural
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import sys
from pathlib import Path

# Agregar el directorio raíz al path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.supabase_client import obtener_respuestas_encuesta
from utils.preguntas_encuesta import PREGUNTAS_TEXTO_LARGO, obtener_pregunta_por_id

st.set_page_config(
    page_title="Análisis de Sentimientos JII 2025",
    page_icon="💬",
    layout="wide"
)

st.title("Análisis de Sentimientos - Jornada de Ingeniería Industrial 2025")
st.markdown("Análisis de respuestas de texto largo mediante procesamiento de lenguaje natural")

# Cargar todas las respuestas de encuesta
with st.spinner("Cargando respuestas de encuesta..."):
    df_respuestas = obtener_respuestas_encuesta()

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
participantes_texto = df_texto['participante_email'].nunique()
preguntas_texto = df_texto['pregunta_id'].nunique()
promedio_longitud = df_texto['respuesta'].str.len().mean()

col1.metric("Total de Respuestas de Texto", total_respuestas_texto)
col2.metric("Participantes Únicos", participantes_texto)
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
        
        # Mostrar todas las respuestas en un expander
        with st.expander("Ver todas las respuestas", expanded=False):
            for idx, row in df_pregunta.iterrows():
                st.markdown(f"**Participante:** {row['nombre_completo']}")
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
    st.markdown("### Análisis de Sentimientos Básico")
    st.info("""
    **Nota:** Este análisis utiliza un enfoque básico basado en palabras clave.
    Para un análisis más preciso, se recomienda integrar modelos de NLP avanzados.
    """)
    
    # Selector de pregunta
    pregunta_seleccionada_sent = st.selectbox(
        "Selecciona una pregunta para análisis de sentimientos",
        options=list(preguntas_opciones.keys()),
        key="sent_selector"
    )
    
    pregunta_id_sent = preguntas_opciones[pregunta_seleccionada_sent]
    df_pregunta_sent = df_texto[df_texto['pregunta_id'] == pregunta_id_sent]
    
    if not df_pregunta_sent.empty:
        # Palabras clave para clasificación básica
        palabras_positivas = {
            'excelente', 'bueno', 'buena', 'increíble', 'genial', 'fantástico', 'maravilloso',
            'perfecto', 'impresionante', 'útil', 'interesante', 'motivador', 'inspirador',
            'profesional', 'calidad', 'aprendí', 'enriquecedor', 'valioso', 'gratificante',
            'satisfactorio', 'positivo', 'destacado', 'sobresaliente', 'relevante'
        }
        
        palabras_negativas = {
            'malo', 'mala', 'terrible', 'pésimo', 'deficiente', 'inadecuado', 'insuficiente',
            'problemático', 'confuso', 'aburrido', 'desorganizado', 'poco', 'falta', 'mejorar',
            'negativo', 'deficiente', 'escaso', 'limitado', 'débil', 'ineficiente'
        }
        
        # Clasificar respuestas
        def clasificar_sentimiento(texto):
            texto_lower = texto.lower()
            puntos_positivos = sum(1 for palabra in palabras_positivas if palabra in texto_lower)
            puntos_negativos = sum(1 for palabra in palabras_negativas if palabra in texto_lower)
            
            if puntos_positivos > puntos_negativos:
                return 'Positivo'
            elif puntos_negativos > puntos_positivos:
                return 'Negativo'
            else:
                return 'Neutral'
        
        df_pregunta_sent['sentimiento'] = df_pregunta_sent['respuesta'].apply(clasificar_sentimiento)
        
        # Estadísticas
        conteo_sentimientos = df_pregunta_sent['sentimiento'].value_counts()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Gráfico de torta
            fig_sent = px.pie(
                values=conteo_sentimientos.values,
                names=conteo_sentimientos.index,
                title='Distribución de Sentimientos',
                color=conteo_sentimientos.index,
                color_discrete_map={
                    'Positivo': '#28a745',
                    'Neutral': '#ffc107',
                    'Negativo': '#dc3545'
                }
            )
            st.plotly_chart(fig_sent, use_container_width=True)
        
        with col2:
            st.markdown("#### Resumen")
            for sentimiento, cantidad in conteo_sentimientos.items():
                porcentaje = (cantidad / len(df_pregunta_sent)) * 100
                st.metric(sentimiento, cantidad, f"{porcentaje:.1f}%")
        
        # Mostrar ejemplos por sentimiento
        st.markdown("---")
        st.markdown("#### Ejemplos de Respuestas por Sentimiento")
        
        sent_tabs = st.tabs(["Positivo", "Neutral", "Negativo"])
        
        for idx, (tab, sentimiento) in enumerate(zip(sent_tabs, ['Positivo', 'Neutral', 'Negativo'])):
            with tab:
                respuestas_sent = df_pregunta_sent[df_pregunta_sent['sentimiento'] == sentimiento]
                if not respuestas_sent.empty:
                    num_mostrar = min(5, len(respuestas_sent))
                    st.markdown(f"**Mostrando {num_mostrar} de {len(respuestas_sent)} respuestas**")
                    for _, row in respuestas_sent.head(num_mostrar).iterrows():
                        with st.expander(f"Respuesta de {row['nombre_completo'][:20]}..."):
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
