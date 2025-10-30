"""
Cliente de Supabase para el Dashboard JII 2025
Proporciona funciones para consultar las tablas de la base de datos.
"""

import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd

# Cargar variables de entorno
load_dotenv()

@st.cache_resource
def get_supabase_client() -> Client:
    """
    Crea y retorna un cliente de Supabase.
    Las credenciales deben estar en las variables de entorno:
    - SUPABASE_URL
    - SUPABASE_KEY
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        st.error("❌ Faltan credenciales de Supabase. Configura SUPABASE_URL y SUPABASE_KEY en el archivo .env")
        st.stop()
    
    return create_client(url, key)


def ejecutar_query(tabla: str, columnas: str = "*", filtros: dict = None, orden: str = None) -> pd.DataFrame:
    """
    Ejecuta una consulta a Supabase y retorna un DataFrame de pandas.
    
    Args:
        tabla: Nombre de la tabla a consultar
        columnas: Columnas a seleccionar (por defecto "*")
        filtros: Diccionario con filtros {columna: valor}
        orden: Columna por la cual ordenar
        
    Returns:
        DataFrame con los resultados
    """
    try:
        supabase = get_supabase_client()
        query = supabase.table(tabla).select(columnas)
        
        # Aplicar filtros si existen
        if filtros:
            for columna, valor in filtros.items():
                query = query.eq(columna, valor)
        
        # Aplicar ordenamiento si existe
        if orden:
            query = query.order(orden)
        
        # Ejecutar query
        response = query.execute()
        
        # Convertir a DataFrame
        if response.data:
            return pd.DataFrame(response.data)
        else:
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Error al ejecutar query en tabla {tabla}: {e}")
        return pd.DataFrame()


def obtener_participantes() -> pd.DataFrame:
    """Obtiene todos los participantes registrados"""
    return ejecutar_query("participantes", orden="created_at")


def obtener_actividades() -> pd.DataFrame:
    """Obtiene todas las actividades"""
    return ejecutar_query("actividades", orden="fecha_inicio")


def obtener_inscripciones_workshop() -> pd.DataFrame:
    """Obtiene todas las inscripciones a workshops"""
    return ejecutar_query("asistencias", orden="created_at")


def obtener_equipos_concurso() -> pd.DataFrame:
    """Obtiene todos los equipos del concurso"""
    return ejecutar_query("equipos_concurso", orden="fecha_registro")


def obtener_respuestas_encuesta() -> pd.DataFrame:
    """Obtiene todas las respuestas de la encuesta"""
    return ejecutar_query("encuesta_respuestas", orden="timestamp")


def obtener_respuestas_por_pregunta(pregunta_id: int) -> pd.DataFrame:
    """
    Obtiene las respuestas de una pregunta específica
    
    Args:
        pregunta_id: ID de la pregunta
        
    Returns:
        DataFrame con las respuestas de esa pregunta
    """
    return ejecutar_query(
        "encuesta_respuestas",
        filtros={"pregunta_id": pregunta_id},
        orden="timestamp"
    )


def obtener_estadisticas_participacion() -> dict:
    """
    Calcula estadísticas generales de participación
    
    Returns:
        Diccionario con métricas clave
    """
    try:
        participantes = obtener_participantes()
        inscripciones = obtener_inscripciones_workshop()
        equipos = obtener_equipos_concurso()
        respuestas = obtener_respuestas_encuesta()
        
        return {
            "total_participantes": len(participantes),
            "total_inscripciones": len(inscripciones),
            "total_equipos": len(equipos),
            "total_respuestas_encuesta": len(respuestas),
            "participantes_con_encuesta": len(participantes[participantes["encuesta_completada"] == True]) if not participantes.empty else 0
        }
    except Exception as e:
        st.error(f"Error al calcular estadísticas: {e}")
        return {}
