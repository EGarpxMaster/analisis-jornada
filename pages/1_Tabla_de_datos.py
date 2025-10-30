"""
Página de Datos Generales - Dashboard JII2025
Visualización de tablas y estadísticas generales del evento
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Agregar el directorio raíz al path para poder importar utils
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.supabase_client import (
    obtener_participantes,
    obtener_inscripciones_workshop,
    obtener_equipos_concurso,
    obtener_actividades
)

st.set_page_config(page_title="Tablas de Datos JII 2025", layout="wide")

st.title("Tablas de Datos - Jornada de Ingeniería Industrial 2025")
st.markdown("Consulta de datos en tiempo real desde Supabase")
st.divider()

# Tabs para organizar las tablas
tab1, tab2, tab3, tab4 = st.tabs([
    "Participantes", 
    "Asistencias", 
    "Equipos Concurso",
    "Actividades"
])

with tab1:
    st.subheader("Participantes Registrados")
    with st.spinner("Cargando datos de participantes..."):
        df_participantes = obtener_participantes()
        
    if not df_participantes.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Participantes", len(df_participantes))
        col2.metric("Encuestas Completadas", 
                   len(df_participantes[df_participantes["encuesta_completada"] == True]))
        col3.metric("Con Brazalete", 
                   len(df_participantes[df_participantes["brazalete"].notna()]))
        
        st.dataframe(df_participantes, use_container_width=True)
        
        # Opción de descarga
        csv = df_participantes.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="participantes_jii2025.csv",
            mime="text/csv"
        )
    else:
        st.info("No hay datos de participantes disponibles")

with tab2:
    st.subheader("Asistencias a Actividades")
    with st.spinner("Cargando datos de asistencias..."):
        df_inscripciones = obtener_inscripciones_workshop()
        
    if not df_inscripciones.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total asistencias", len(df_inscripciones))
        
        st.dataframe(df_inscripciones, use_container_width=True)
        
        # Opción de descarga
        csv = df_inscripciones.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="inscripciones_jii2025.csv",
            mime="text/csv"
        )
    else:
        st.info("No hay datos de inscripciones disponibles")

with tab3:
    st.subheader("Equipos del Concurso")
    with st.spinner("Cargando datos de equipos..."):
        df_equipos = obtener_equipos_concurso()
        
    if not df_equipos.empty:
        col1, col2 = st.columns(2)
        col1.metric("Total Equipos", len(df_equipos))
        
        # Contar por estado de registro
        if "estado_registro" in df_equipos.columns:
            estados = df_equipos["estado_registro"].value_counts()
        
        st.dataframe(df_equipos, use_container_width=True)
        
        # Opción de descarga
        csv = df_equipos.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="equipos_concurso_jii2025.csv",
            mime="text/csv"
        )
    else:
        st.info("No hay datos de equipos disponibles")

with tab4:
    st.subheader("Actividades Programadas")
    with st.spinner("Cargando datos de actividades..."):
        df_actividades = obtener_actividades()
        
    if not df_actividades.empty:
        col1, col2 = st.columns(2)
        col1.metric("Total Actividades", len(df_actividades))
        
        # Contar por tipo
        if "tipo" in df_actividades.columns:
            tipos = df_actividades["tipo"].value_counts()
            col2.metric("Tipos de Actividades", len(tipos))
        
        st.dataframe(df_actividades, use_container_width=True)
        
        # Opción de descarga
        csv = df_actividades.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="actividades_jii2025.csv",
            mime="text/csv"
        )
    else:
        st.info("No hay datos de actividades disponibles")
