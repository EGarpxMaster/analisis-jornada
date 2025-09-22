import streamlit as st
import pandas as pd
import pymysql
import pymysql.err as pymysql_err
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Jornada II",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para conectar a la base de datos
@st.cache_resource
def init_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', '192.168.200.212'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'industrial'),
            password=os.getenv('DB_PASSWORD', 'p@ss4DB'),
            database=os.getenv('DB_DATABASE', 'jornada_ii'),
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql_err.MySQLError as e:
        st.error(f"Error conectando a la base de datos: {e}")
        return None

# ===============================================
# TABLA DE DATOS EN STREAMLIT
# ===============================================

def run_query(query: str):
    """Ejecuta un query y devuelve un DataFrame."""
    conn = init_connection()
    if conn is None:
        return pd.DataFrame()  # si falla la conexión, regresa vacío
    
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
        return pd.DataFrame(result)
    except pymysql_err.MySQLError as e:
        st.error(f"Error ejecutando query: {e}")
        return pd.DataFrame()


# Participantes
st.subheader("📋 Lista de Participantes")
df_participantes = run_query("""
    SELECT 
        id,
        CONCAT(primer_nombre, ' ', COALESCE(segundo_nombre, ''), ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
        email,
        categoria,
        programa,
        brazalete
    FROM participantes
    ORDER BY creado DESC
""")
st.dataframe(df_participantes, use_container_width=True)

# Inscripciones Workshop
st.subheader("📝 Inscripciones a Workshops")
df_inscripciones = run_query("""
    SELECT iw.id, p.email AS participante_email, a.codigo AS actividad_codigo, iw.estado, iw.creado
    FROM inscripciones_workshop iw
    JOIN participantes p ON iw.participante_id = p.id
    JOIN actividades a ON iw.actividad_id = a.id
    ORDER BY iw.creado DESC
""")
st.dataframe(df_inscripciones, use_container_width=True)

# Asistencias
st.subheader("✅ Asistencias")
df_asistencias = run_query("""
    SELECT a.id, p.email AS participante_email, act.codigo AS actividad_codigo, a.estado, a.modo_asistencia, a.fecha_asistencia, a.notas
    FROM asistencias a
    JOIN participantes p ON a.participante_id = p.id
    JOIN actividades act ON a.actividad_id = act.id
    ORDER BY a.fecha_asistencia DESC
""")
st.dataframe(df_asistencias, use_container_width=True)

# Equipos Concurso
st.subheader("🏆 Equipos Concurso")
df_equipos = run_query("""
    SELECT id, nombre_equipo, estado_id, email_capitan, estado_registro, activo, fecha_registro, fecha_confirmacion
    FROM equipos_concurso
    ORDER BY fecha_registro DESC
""")
st.dataframe(df_equipos, use_container_width=True)
