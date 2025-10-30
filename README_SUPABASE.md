# Dashboard JII 2025 - Configuración de Supabase

## Paso 1: Crear archivo .env

Crea un archivo `.env` en la raíz del proyecto con tus credenciales de Supabase:

```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_anon_key_aqui
```

## Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Configurar TextBlob para Análisis de Sentimientos

Para habilitar el análisis de sentimientos avanzado:

```bash
pip install textblob
python -m textblob.download_corpora
```

Ver [README_TEXTBLOB.md](README_TEXTBLOB.md) para más detalles.

## Paso 3: Ejecutar la aplicación localmente

```bash
streamlit run app.py
```

## Paso 4: Desplegar en Streamlit Cloud

1. Sube el repositorio a GitHub
2. Ve a https://share.streamlit.io/
3. Conecta tu repositorio
4. En "Advanced settings", agrega tus secretos:
   ```
   SUPABASE_URL = "https://tu-proyecto.supabase.co"
   SUPABASE_KEY = "tu_anon_key_aqui"
   ```
5. Despliega

## Estructura del proyecto

```
analisis-jornada/
├── app.py                          # Página principal
├── pages/                          # Páginas del dashboard
│   ├── 1_Tabla_de_datos_new.py    # Tablas de datos
│   ├── 2_Dashboard.py              # Dashboard con visualizaciones
│   ├── 3_Analisis_Encuesta.py     # Análisis de encuestas
│   └── 4_Analisis_Sentimientos.py # Análisis de sentimientos
├── utils/                          # Utilidades
│   ├── supabase_client.py         # Cliente de Supabase
│   └── preguntas_encuesta.py      # Definición de preguntas
├── requirements.txt                # Dependencias
├── .env                            # Credenciales (NO subir a git)
└── .env.example                    # Ejemplo de credenciales
```

## Funcionalidades principales

### 📊 Análisis de Datos
- **Tablas de datos**: Visualiza participantes, inscripciones, equipos y actividades
- **Dashboard**: KPIs y gráficos interactivos con Plotly
- **Evolución temporal**: Análisis de asistencias y registro de equipos por hora/día

### 📈 Análisis de Encuestas
- **Cuantitativo**: Análisis de calificaciones 1-5 con estadísticas y gráficos
- **Cualitativo**: Análisis de respuestas de texto largo
- **Privacidad**: Todas las respuestas son **anónimas** (no se muestran emails ni nombres)

### 💬 Análisis de Sentimientos Avanzado
- **TextBlob NLP**: Análisis de polaridad (-1 a +1) y subjetividad (0 a 1)
- **Visualizaciones**: Scatter plots, histogramas, distribuciones
- **Clasificación automática**: Positivo, Neutral, Negativo
- **Ejemplos ordenados**: Por nivel de polaridad

## Notas importantes

- NO subas el archivo `.env` a Git
- Agrega `.env` a tu `.gitignore`
- Las credenciales de Supabase están en: Supabase Dashboard > Settings > API
- Las respuestas de encuestas se muestran de forma **anónima** para proteger la privacidad
- El análisis temporal detecta automáticamente si usar agrupación por hora o por día
