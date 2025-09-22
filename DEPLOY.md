# Instrucciones para desplegar en GitHub + Streamlit Cloud

1. **Estructura**: El archivo principal es `MultiPage App/app.py`.
2. **Requisitos**: Todos los paquetes necesarios están en `requirements.txt`.
3. **Procfile**: Ya incluido para plataformas como Heroku/Streamlit Cloud.
4. **Configuración extra**: `.streamlit/config.toml` incluido para personalización y compatibilidad.

## Despliegue en Streamlit Cloud

1. Sube este repositorio a GitHub.
2. Ve a https://share.streamlit.io/ y conecta tu cuenta de GitHub.
3. Selecciona el repositorio y pon como archivo principal:
   
   ```
   MultiPage App/app.py
   ```
4. ¡Listo! Streamlit detectará automáticamente `requirements.txt` y la configuración.

## Notas
- Si usas otra plataforma (Heroku, etc.), el `Procfile` también funcionará.
- Si agregas nuevas dependencias, recuerda actualizar `requirements.txt`.
- Los datos deben estar en la carpeta `MultiPage App/datos/`.

---

¿Dudas? Consulta la documentación oficial de Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
