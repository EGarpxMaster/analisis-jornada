"""
Análisis de Encuesta - Jornada de Ingeniería Industrial 2025
Análisis cuantitativo de respuestas de calificación (1-5)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# Agregar el directorio raíz al path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.supabase_client import obtener_respuestas_encuesta, obtener_respuestas_por_pregunta
from utils.preguntas_encuesta import PREGUNTAS_CALIFICACION, TODAS_PREGUNTAS, obtener_pregunta_por_id

st.set_page_config(
    page_title="Análisis de Encuesta JII 2025",
    page_icon="📊",
    layout="wide"
)

st.title("Análisis de Encuesta - Jornada de Ingeniería Industrial 2025")
st.markdown("Análisis cuantitativo de respuestas de calificación")

# Cargar todas las respuestas de encuesta
with st.spinner("Cargando respuestas de encuesta..."):
    df_respuestas = obtener_respuestas_encuesta()

if df_respuestas.empty:
    st.warning("No hay respuestas de encuesta disponibles")
    st.stop()

# Estadísticas generales
st.subheader("Estadísticas Generales")
col1, col2, col3, col4 = st.columns(4)

total_respuestas = len(df_respuestas)
participantes_unicos = df_respuestas['participante_email'].nunique()
preguntas_respondidas = df_respuestas['pregunta_id'].nunique()

col1.metric("Total de Respuestas", total_respuestas)
col2.metric("Participantes Únicos", participantes_unicos)
col3.metric("Preguntas Respondidas", preguntas_respondidas)
col4.metric("Promedio Respuestas/Participante", round(total_respuestas / participantes_unicos, 1))

st.markdown("---")

# Filtrar solo preguntas de calificación
ids_calificacion = [p['id'] for p in PREGUNTAS_CALIFICACION]
df_calificaciones = df_respuestas[df_respuestas['pregunta_id'].isin(ids_calificacion)].copy()

# Convertir respuestas a numérico
df_calificaciones['respuesta_num'] = pd.to_numeric(df_calificaciones['respuesta'], errors='coerce')

# Análisis por pregunta
st.subheader("Análisis por Pregunta de Calificación (1-5)")

# Tabs para diferentes análisis
tab1, tab2, tab3 = st.tabs(["Promedios por Pregunta", "Distribución de Respuestas", "Análisis Detallado"])

with tab1:
    st.markdown("### Calificaciones Promedio por Pregunta")
    
    # Calcular promedios
    promedios = df_calificaciones.groupby(['pregunta_id', 'pregunta_texto'])['respuesta_num'].agg([
        ('promedio', 'mean'),
        ('total', 'count'),
        ('desv_std', 'std')
    ]).reset_index()
    
    promedios = promedios.sort_values('promedio', ascending=True)
    
    # Gráfico de barras horizontales
    fig_promedios = px.bar(
        promedios,
        y='pregunta_texto',
        x='promedio',
        orientation='h',
        text='promedio',
        title='Calificación Promedio por Pregunta',
        color='promedio',
        color_continuous_scale='RdYlGn',
        range_color=[1, 5]
    )
    
    fig_promedios.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_promedios.update_layout(
        xaxis_title="Calificación Promedio",
        yaxis_title="",
        height=max(400, len(promedios) * 40),
        showlegend=False
    )
    
    st.plotly_chart(fig_promedios, use_container_width=True)
    
    # Tabla de datos
    st.markdown("### Tabla de Resultados")
    promedios_display = promedios.copy()
    promedios_display['promedio'] = promedios_display['promedio'].round(2)
    promedios_display['desv_std'] = promedios_display['desv_std'].round(2)
    promedios_display.columns = ['ID Pregunta', 'Pregunta', 'Promedio', 'Total Respuestas', 'Desviación Estándar']
    
    st.dataframe(promedios_display, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("### Distribución de Respuestas por Pregunta")
    
    # Selector de pregunta
    preguntas_opciones = {f"{p['id']}: {p['texto'][:60]}...": p['id'] for p in PREGUNTAS_CALIFICACION}
    pregunta_seleccionada = st.selectbox(
        "Selecciona una pregunta",
        options=list(preguntas_opciones.keys())
    )
    
    pregunta_id = preguntas_opciones[pregunta_seleccionada]
    pregunta_info = obtener_pregunta_por_id(pregunta_id)
    
    # Filtrar respuestas de la pregunta seleccionada
    df_pregunta = df_calificaciones[df_calificaciones['pregunta_id'] == pregunta_id]
    
    if not df_pregunta.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Histograma de distribución
            distribucion = df_pregunta['respuesta_num'].value_counts().sort_index()
            
            fig_dist = px.bar(
                x=distribucion.index,
                y=distribucion.values,
                labels={'x': 'Calificación', 'y': 'Cantidad'},
                title=f"Distribución de Respuestas: {pregunta_info['texto'][:80]}...",
                text=distribucion.values
            )
            
            fig_dist.update_traces(textposition='outside', marker_color='steelblue')
            fig_dist.update_layout(
                xaxis=dict(tickmode='linear', tick0=1, dtick=1),
                showlegend=False
            )
            
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with col2:
            # Estadísticas de la pregunta
            st.markdown("#### Estadísticas")
            promedio = df_pregunta['respuesta_num'].mean()
            mediana = df_pregunta['respuesta_num'].median()
            moda = df_pregunta['respuesta_num'].mode().iloc[0] if not df_pregunta['respuesta_num'].mode().empty else 0
            desv_std = df_pregunta['respuesta_num'].std()
            total = len(df_pregunta)
            
            st.metric("Promedio", f"{promedio:.2f}")
            st.metric("Mediana", f"{mediana:.1f}")
            st.metric("Moda", f"{moda:.0f}")
            st.metric("Desviación Estándar", f"{desv_std:.2f}")
            st.metric("Total Respuestas", total)
            
            # Porcentajes por calificación
            st.markdown("#### Porcentajes")
            porcentajes = (df_pregunta['respuesta_num'].value_counts(normalize=True) * 100).sort_index()
            for cal, pct in porcentajes.items():
                st.write(f"**{int(cal)}:** {pct:.1f}%")
    else:
        st.info("No hay respuestas para esta pregunta")

with tab3:
    st.markdown("### Análisis Detallado por Categoría de Pregunta")
    
    # Agrupar preguntas por categoría (Generales, Workshop, Mundialito)
    from utils.preguntas_encuesta import PREGUNTAS_GENERALES, PREGUNTAS_WORKSHOP, PREGUNTAS_MUNDIALITO
    
    categorias = {
        "Preguntas Generales": [p['id'] for p in PREGUNTAS_GENERALES if p['tipo'] == 'calificacion_1_5'],
        "Workshop": [p['id'] for p in PREGUNTAS_WORKSHOP if p['tipo'] == 'calificacion_1_5'],
        "Mundialito Mexicano": [p['id'] for p in PREGUNTAS_MUNDIALITO if p['tipo'] == 'calificacion_1_5']
    }
    
    # Calcular promedios por categoría
    resultados_categoria = []
    
    for categoria, pregunta_ids in categorias.items():
        df_cat = df_calificaciones[df_calificaciones['pregunta_id'].isin(pregunta_ids)]
        if not df_cat.empty:
            promedio = df_cat['respuesta_num'].mean()
            total = len(df_cat)
            resultados_categoria.append({
                'Categoría': categoria,
                'Promedio': promedio,
                'Total Respuestas': total
            })
    
    if resultados_categoria:
        df_categorias = pd.DataFrame(resultados_categoria)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Gráfico de barras por categoría
            fig_cat = px.bar(
                df_categorias,
                x='Categoría',
                y='Promedio',
                text='Promedio',
                title='Calificación Promedio por Categoría',
                color='Promedio',
                color_continuous_scale='RdYlGn',
                range_color=[1, 5]
            )
            
            fig_cat.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_cat.update_layout(showlegend=False, yaxis_range=[0, 5.5])
            
            st.plotly_chart(fig_cat, use_container_width=True)
        
        with col2:
            # Gráfico de radar
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=df_categorias['Promedio'].tolist() + [df_categorias['Promedio'].iloc[0]],
                theta=df_categorias['Categoría'].tolist() + [df_categorias['Categoría'].iloc[0]],
                fill='toself',
                name='Promedio'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )
                ),
                title='Comparativa por Categoría',
                showlegend=True
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("No hay datos suficientes para análisis por categoría")

# Descargar datos
st.markdown("---")
st.subheader("Exportar Datos")

col1, col2 = st.columns(2)

with col1:
    if not df_calificaciones.empty:
        csv_calificaciones = df_calificaciones.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Calificaciones (CSV)",
            data=csv_calificaciones,
            file_name="calificaciones_encuesta_jii2025.csv",
            mime="text/csv"
        )

with col2:
    if not promedios.empty:
        csv_promedios = promedios.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Promedios (CSV)",
            data=csv_promedios,
            file_name="promedios_encuesta_jii2025.csv",
            mime="text/csv"
        )

st.markdown("---")
st.caption("Dashboard JII 2025 - Análisis de Encuesta")
