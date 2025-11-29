from app.extensions import db
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, DECIMAL, Text
from sqlalchemy.sql import func

class EncuestaUsabilidad(db.Model):
    __tablename__ = "encuesta_usabilidad"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False)
    rol_usuario =Column(Integer, nullable=False)
    fecha_encuesta = Column(TIMESTAMP, server_default=func.now())

    # Sección 1: Facilidad de Uso
    navegacion_clara = Column(Integer)
    facil_encontrar_funciones = Column(Integer)
    instrucciones_claras = Column(Integer)
    aprendizaje_rapido = Column(Integer)

    # Sección 2: Eficiencia
    tareas_rapidas = Column(Integer)
    pocos_pasos = Column(Integer)
    proceso_citas_agil = Column(Integer)
    registro_eficiente = Column(Integer)

    # Sección 3: Atracción
    diseno_atractivo = Column(Integer)
    colores_agradables = Column(Integer)
    iconos_modernos = Column(Integer)
    aspecto_general = Column(Integer)

    # Sección 4: Inclusivo
    texto_comodo = Column(Integer)
    contrastes_adecuados = Column(Integer)
    diseno_inclusivo = Column(Integer)
    lenguaje_respetuoso = Column(Integer)

    # Sección 5: Evitar Frustración
    proteccion_errores = Column(Integer)
    mensajes_error_claros = Column(Integer)
    respuesta_consistente = Column(Integer)
    control_tranquilidad = Column(Integer)

    # Sección 6: Satisfacción General
    satisfaccion_general = Column(Integer)
    herramienta_util = Column(Integer)
    recomendaria_aplicacion = Column(Integer)
    sentir_apoyado = Column(Integer)

    # Preguntas Abiertas
    que_mas_gusto = Column(Text)
    que_mejorar = Column(Text)
    que_confuso_frustrante = Column(Text)

    # Metadatos adicionales
    puntuacion_total = Column(Integer)
    promedio_seccion = Column(DECIMAL(3, 2))
    completada = Column(Boolean, default=False)
