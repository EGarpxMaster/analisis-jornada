
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

st.set_page_config(
	page_title="Análisis Jornada II",
	page_icon="📊",
	layout="wide",
	initial_sidebar_state="expanded"
)

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

def run_query(query: str):
	conn = init_connection()
	if conn is None:
		return pd.DataFrame()
	try:
		with conn.cursor() as cur:
			cur.execute(query)
			result = cur.fetchall()
		return pd.DataFrame(result)
	except pymysql_err.MySQLError as e:
		st.error(f"Error ejecutando query: {e}")
		return pd.DataFrame()

# =====================
# KPIs principales
# =====================
st.title("📊 Dashboard de Análisis Jornada II")

# Participantes
df_participantes = run_query("""
	SELECT id, categoria, programa, creado FROM participantes
""")

# Inscripciones Workshop
df_inscripciones = run_query("""
	SELECT id, estado, creado FROM inscripciones_workshop
""")

# Asistencias
df_asistencias = run_query("""
	SELECT id, estado, modo_asistencia, fecha_asistencia FROM asistencias
""")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Participantes registrados", len(df_participantes))
col2.metric("Inscripciones a Workshops", len(df_inscripciones))
col3.metric("Registros de Asistencia", len(df_asistencias))

st.markdown("---")

# =====================
# Análisis por categoría de participante
# =====================
st.subheader("Distribución de Participantes por Categoría")
if not df_participantes.empty:
	cat_counts = df_participantes['categoria'].value_counts().reset_index()
	cat_counts.columns = ['Categoría', 'Cantidad']
	fig_cat = px.bar(cat_counts, x='Categoría', y='Cantidad', color='Categoría', text='Cantidad')
	st.plotly_chart(fig_cat, use_container_width=True)
else:
	st.info("No hay datos de participantes.")

# =====================
# Análisis por programa académico
# =====================
st.subheader("Distribución de Participantes por Programa Académico")
if not df_participantes.empty:
	prog_counts = df_participantes['programa'].value_counts().reset_index()
	prog_counts.columns = ['Programa', 'Cantidad']
	fig_prog = px.pie(prog_counts, names='Programa', values='Cantidad', hole=0.4)
	st.plotly_chart(fig_prog, use_container_width=True)
else:
	st.info("No hay datos de participantes.")

# =====================
# Inscripciones a Workshops por estado
# =====================
st.subheader("Estado de Inscripciones a Workshops")
if not df_inscripciones.empty:
	insc_counts = df_inscripciones['estado'].value_counts().reset_index()
	insc_counts.columns = ['Estado', 'Cantidad']
	fig_insc = px.bar(insc_counts, x='Estado', y='Cantidad', color='Estado', text='Cantidad')
	st.plotly_chart(fig_insc, use_container_width=True)
else:
	st.info("No hay datos de inscripciones a workshops.")
