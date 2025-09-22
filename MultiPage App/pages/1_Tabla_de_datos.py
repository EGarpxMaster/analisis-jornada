import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Tablas de Datos CSV", layout="wide")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "datos"

csv_files = [
    ("Participantes", "participantes.csv"),
    ("Inscripciones a Workshops", "inscripciones_workshop.csv"),
    ("Equipos Concurso", "equipos_concurso.csv"),
    ("Asistencias", "asistencias.csv")
]

st.title("Tablas de datos")
st.divider()

for titulo, filename in csv_files:
    file_path = DATA_DIR / filename
    st.subheader(f"{titulo}")
    if file_path.exists():
        if file_path.stat().st_size == 0:
            st.warning(f"El archivo está vacío: {file_path}")
        else:
            try:
                df = pd.read_csv(file_path)
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                if "No columns to parse from file" in str(e):
                    st.warning(f"El archivo está vacío: {file_path}")
                else:
                    st.error(f"Error al leer {file_path}: {e}")
    else:
        st.warning(f"No se encontró el archivo: {file_path}")
