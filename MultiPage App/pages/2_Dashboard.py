
import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Dashboard CSV Jornada II", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "datos"

# Cargar datos
df_participantes = pd.read_csv(DATA_DIR / "participantes.csv") if (DATA_DIR / "participantes.csv").exists() else pd.DataFrame()
df_inscripciones = pd.read_csv(DATA_DIR / "inscripciones_workshop.csv") if (DATA_DIR / "inscripciones_workshop.csv").exists() else pd.DataFrame()
df_equipos = pd.read_csv(DATA_DIR / "equipos_concurso.csv") if (DATA_DIR / "equipos_concurso.csv").exists() else pd.DataFrame()

st.title("📊 Dashboard de Análisis Jornada II (CSV)")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Participantes registrados", len(df_participantes))
col2.metric("Inscripciones a Workshops", len(df_inscripciones))
col3.metric("Equipos registrados", len(df_equipos))

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
st.subheader("Inscripciones por Workshop")
if not df_inscripciones.empty:
    act_counts = df_inscripciones['actividad_codigo'].value_counts().reset_index()
    act_counts.columns = ['Workshop', 'Cantidad']
    fig_act = px.bar(act_counts, x='Workshop', y='Cantidad', color='Workshop', text='Cantidad')
    st.plotly_chart(fig_act, use_container_width=True)
else:
    st.info("No hay datos de inscripciones a workshops.")

# Evolución temporal de inscripciones
st.subheader("Evolución Temporal de Inscripciones a Workshops")
if not df_inscripciones.empty and 'creado' in df_inscripciones.columns:
    df_inscripciones['creado'] = pd.to_datetime(df_inscripciones['creado'], errors='coerce')
    df_inscripciones['fecha'] = df_inscripciones['creado'].dt.date
    fecha_counts = df_inscripciones.groupby('fecha').size().reset_index(name='Cantidad')
    fig_fecha = px.line(fecha_counts, x='fecha', y='Cantidad', markers=True)
    st.plotly_chart(fig_fecha, use_container_width=True)
else:
    st.info("No hay datos de fechas de inscripciones.")

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
    df_equipos['fecha_registro'] = pd.to_datetime(df_equipos['fecha_registro'], errors='coerce')
    df_equipos['fecha'] = df_equipos['fecha_registro'].dt.date
    eq_fecha_counts = df_equipos.groupby('fecha').size().reset_index(name='Cantidad')
    fig_eq_fecha = px.line(eq_fecha_counts, x='fecha', y='Cantidad', markers=True)
    st.plotly_chart(fig_eq_fecha, use_container_width=True)
else:
    st.info("No hay datos de fechas de registro de equipos.")
