"""
Dashboard Principal - Jornada de Ingeniería Industrial 2025
Visualizaciones y análisis de datos del evento desde Supabase
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Agregar el directorio raíz al path para poder importar utils
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.supabase_client import (
    obtener_participantes,
    obtener_inscripciones_workshop,
    obtener_asistencias,
    obtener_equipos_concurso,
    obtener_actividades,
    obtener_estadisticas_participacion
)

st.set_page_config(
    page_title="Dashboard JII 2025", 
    page_icon="📊", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.title("Dashboard de Análisis - Jornada de Ingeniería Industrial 2025")
st.markdown("Análisis en tiempo real de datos del evento")

# Cargar datos desde Supabase
with st.spinner("Cargando datos desde Supabase..."):
    df_participantes = obtener_participantes()
    df_inscripciones = obtener_inscripciones_workshop()
    df_asistencias = obtener_asistencias()  # Para evolución temporal
    df_equipos = obtener_equipos_concurso()
    stats = obtener_estadisticas_participacion()

# KPIs principales
st.subheader("Indicadores Clave")
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Participantes Registrados", 
    stats.get("total_participantes", 0)
)
col2.metric(
    "Inscripciones a Actividades", 
    stats.get("total_inscripciones", 0)
)
col3.metric(
    "Equipos Concurso", 
    stats.get("total_equipos", 0)
)
col4.metric(
    "Encuestas Completadas",
    stats.get("participantes_con_encuesta", 0),
    delta=f"{round(stats.get('participantes_con_encuesta', 0) / max(stats.get('total_participantes', 1), 1) * 100, 1)}%"
)

st.markdown("---")

# Participantes por programa
st.subheader("Participantes por Programa Académico")
if not df_participantes.empty:
    prog_counts = df_participantes['programa'].value_counts().reset_index()
    prog_counts.columns = ['Programa', 'Cantidad']
    fig_prog = px.bar(prog_counts, x='Programa', y='Cantidad', color='Programa', text='Cantidad')
    st.plotly_chart(fig_prog, use_container_width=True)
else:
    st.info("No hay datos de participantes.")

# Participantes por categoría
st.subheader("Participantes por Categoría")
if not df_participantes.empty:
    cat_counts = df_participantes['categoria'].value_counts().reset_index()
    cat_counts.columns = ['Categoría', 'Cantidad']
    fig_cat = px.pie(cat_counts, names='Categoría', values='Cantidad', hole=0.4)
    st.plotly_chart(fig_cat, use_container_width=True)
else:
    st.info("No hay datos de participantes.")

# Inscripciones por estado
st.subheader("Inscripciones a Workshops por Estado")
if not df_inscripciones.empty:
    insc_counts = df_inscripciones['estado'].value_counts().reset_index()
    insc_counts.columns = ['Estado', 'Cantidad']
    fig_insc = px.bar(insc_counts, x='Estado', y='Cantidad', color='Estado', text='Cantidad')
    st.plotly_chart(fig_insc, use_container_width=True)
else:
    st.info("No hay datos de inscripciones a workshops.")

# Inscripciones por actividad
st.subheader("Inscripciones por Actividad")
if not df_inscripciones.empty:
    act_counts = df_inscripciones['actividad_codigo'].value_counts().reset_index()
    act_counts.columns = ['Workshop', 'Cantidad']
    fig_act = px.bar(act_counts, x='Workshop', y='Cantidad', color='Workshop', text='Cantidad')
    st.plotly_chart(fig_act, use_container_width=True)
else:
    st.info("No hay datos de inscripciones a workshops.")

# Evolución temporal de asistencias (dato real)
st.subheader("Evolución Temporal de Asistencias")
if not df_asistencias.empty and 'fecha_asistencia' in df_asistencias.columns:
    df_temp = df_asistencias.copy()
    df_temp['fecha_asistencia'] = pd.to_datetime(df_temp['fecha_asistencia'], errors='coerce')
    
    # Determinar si agrupar por hora o por día según el rango de fechas
    rango_dias = (df_temp['fecha_asistencia'].max() - df_temp['fecha_asistencia'].min()).days
    
    if rango_dias <= 2:  # Si es 2 días o menos, agrupar por hora
        df_temp['periodo'] = df_temp['fecha_asistencia'].dt.floor('h')
        titulo = 'Asistencias por Hora'
        label_x = 'Hora'
    else:  # Si es más de 2 días, agrupar por día
        df_temp['periodo'] = df_temp['fecha_asistencia'].dt.date
        titulo = 'Asistencias por Día'
        label_x = 'Fecha'
    
    periodo_counts = df_temp.groupby('periodo').size().reset_index(name='Cantidad')
    
    fig_asist = px.line(
        periodo_counts, 
        x='periodo', 
        y='Cantidad', 
        markers=True, 
        title=titulo,
        labels={'periodo': label_x, 'Cantidad': 'Número de Asistencias'}
    )
    fig_asist.update_traces(line_color='#1f77b4', line_width=2, marker=dict(size=8))
    fig_asist.update_layout(hovermode='x unified')
    st.plotly_chart(fig_asist, use_container_width=True)
else:
    st.info("No hay datos de fechas de asistencias.")

# Equipos por estado_registro
st.subheader("Equipos por Estado de Registro")
if not df_equipos.empty and 'estado_registro' in df_equipos.columns:
    eq_counts = df_equipos['estado_registro'].value_counts().reset_index()
    eq_counts.columns = ['Estado de Registro', 'Cantidad']
    fig_eq = px.bar(eq_counts, x='Estado de Registro', y='Cantidad', color='Estado de Registro', text='Cantidad')
    st.plotly_chart(fig_eq, use_container_width=True)
else:
    st.info("No hay datos de equipos.")

# Evolución temporal de equipos registrados
st.subheader("Evolución Temporal de Registro de Equipos")
if not df_equipos.empty and 'fecha_registro' in df_equipos.columns:
    df_equipos_temp = df_equipos.copy()
    df_equipos_temp['fecha_registro'] = pd.to_datetime(df_equipos_temp['fecha_registro'], errors='coerce')
    
    # Determinar si agrupar por hora o por día según el rango de fechas
    rango_dias_eq = (df_equipos_temp['fecha_registro'].max() - df_equipos_temp['fecha_registro'].min()).days
    
    if rango_dias_eq <= 2:  # Si es 2 días o menos, agrupar por hora
        df_equipos_temp['periodo'] = df_equipos_temp['fecha_registro'].dt.floor('h')
        titulo_eq = 'Registro de Equipos por Hora'
        label_x_eq = 'Hora'
    else:  # Si es más de 2 días, agrupar por día
        df_equipos_temp['periodo'] = df_equipos_temp['fecha_registro'].dt.date
        titulo_eq = 'Registro de Equipos por Día'
        label_x_eq = 'Fecha'
    
    eq_fecha_counts = df_equipos_temp.groupby('periodo').size().reset_index(name='Cantidad')
    
    fig_eq_fecha = px.line(
        eq_fecha_counts, 
        x='periodo', 
        y='Cantidad', 
        markers=True,
        title=titulo_eq,
        labels={'periodo': label_x_eq, 'Cantidad': 'Número de Equipos'}
    )
    fig_eq_fecha.update_traces(line_color='#ff7f0e', line_width=2, marker=dict(size=8))
    fig_eq_fecha.update_layout(hovermode='x unified')
    st.plotly_chart(fig_eq_fecha, use_container_width=True)
else:
    st.info("No hay datos de fechas de registro de equipos.")
