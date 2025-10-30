"""
Definición de preguntas de la encuesta JII 2025
"""

# Preguntas generales de la encuesta
PREGUNTAS_GENERALES = [
    {"id": 1, "texto": "¿Cómo calificas la organización de la JII?", "tipo": "calificacion_1_5"},
    {"id": 2, "texto": "¿Cómo calificas los horarios de la JII?", "tipo": "calificacion_1_5"},
    {"id": 3, "texto": "¿Cómo calificas la duración de las actividades?", "tipo": "calificacion_1_5"},
    {"id": 4, "texto": "Especifica la razón principal por la que asististe a la JII:", "tipo": "texto_corto"},
    {"id": 5, "texto": "¿Cumplieron tus expectativas las actividades en las que participaste?", "tipo": "calificacion_1_5"},
    {"id": 6, "texto": "¿Los contenidos desarrollados resultaron útiles?", "tipo": "calificacion_1_5"},
    {"id": 7, "texto": "¿Qué tan relevante consideras que fue el nivel profesional de la JII?", "tipo": "calificacion_1_5"},
    {"id": 8, "texto": "¿Qué conferencia magistral te pareció la más relevante?", "tipo": "select_conferencia"},
    {"id": 10, "texto": "¿Qué actividad consideras que fue la de mayor relevancia?", "tipo": "select_tipo_actividad"},
    {"id": 11, "texto": "¿Cuáles fueron para ti los puntos fuertes de la JII? ¿Por qué?", "tipo": "texto_largo"},
    {"id": 12, "texto": "¿Qué parte te gustó menos? ¿Por qué?", "tipo": "texto_largo"},
    {"id": 13, "texto": "Propón tres temas de tu interés para la edición 2026 de la JII.", "tipo": "texto_largo"},
    {"id": 14, "texto": "¿Qué sugerencias podrías aportar para mejorar la próxima edición de la JII?", "tipo": "texto_largo"},
    {"id": 15, "texto": "En términos generales, ¿Cómo calificaría la Jornada de Ingeniería Industrial 2025?", "tipo": "calificacion_1_5"},
    {"id": 16, "texto": "Comentarios adicionales:", "tipo": "texto_largo"},
]

# Preguntas sobre workshops
PREGUNTAS_WORKSHOP = [
    {"id": 17, "texto": "Valora el workshop al que asististe (1=Muy Malo, 5=Excelente)", "tipo": "calificacion_1_5"},
    {"id": 18, "texto": "Comentarios sobre el workshop", "tipo": "texto_largo"},
]

# Preguntas sobre mundialito
PREGUNTAS_MUNDIALITO = [
    {"id": 19, "texto": "Valora el Mundialito Mexicano", "tipo": "calificacion_1_5"},
    {"id": 20, "texto": "Comentarios sobre el Mundialito Mexicano", "tipo": "texto_largo"},
]

# Todas las preguntas combinadas
TODAS_PREGUNTAS = PREGUNTAS_GENERALES + PREGUNTAS_WORKSHOP + PREGUNTAS_MUNDIALITO

# Preguntas de calificación (1-5)
PREGUNTAS_CALIFICACION = [p for p in TODAS_PREGUNTAS if p["tipo"] == "calificacion_1_5"]

# Preguntas de texto largo (para análisis de sentimientos)
PREGUNTAS_TEXTO_LARGO = [p for p in TODAS_PREGUNTAS if p["tipo"] == "texto_largo"]


def obtener_pregunta_por_id(pregunta_id: int) -> dict:
    """
    Obtiene la información de una pregunta por su ID
    
    Args:
        pregunta_id: ID de la pregunta
        
    Returns:
        Diccionario con la información de la pregunta o None si no existe
    """
    for pregunta in TODAS_PREGUNTAS:
        if pregunta["id"] == pregunta_id:
            return pregunta
    return None


def obtener_preguntas_por_tipo(tipo: str) -> list:
    """
    Obtiene todas las preguntas de un tipo específico
    
    Args:
        tipo: Tipo de pregunta (calificacion_1_5, texto_largo, etc.)
        
    Returns:
        Lista de preguntas del tipo especificado
    """
    return [p for p in TODAS_PREGUNTAS if p["tipo"] == tipo]
