"""
Cliente de conexión a Supabase para el Dashboard JII2025
"""
import os
from supabase import create_client, Client
import streamlit as st

@st.cache_resource
def get_supabase_client() -> Client:
    """
    Crea y retorna un cliente de Supabase singleton.
    Las credenciales deben estar en secrets.toml o variables de entorno.
    """
    supabase_url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    supabase_key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        st.error("⚠️ Credenciales de Supabase no configuradas")
        st.stop()
    
    return create_client(supabase_url, supabase_key)

def test_connection() -> bool:
    """Prueba la conexión a Supabase"""
    try:
        client = get_supabase_client()
        # Intenta una consulta simple
        client.table("participantes").select("id").limit(1).execute()
        return True
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return False