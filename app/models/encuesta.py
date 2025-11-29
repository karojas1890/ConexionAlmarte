from app.extensions import db
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func

class EncuestaUsabilidad(db.Model):
    __tablename__ = "encuesta_usabilidad"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False)
    rol_usuario = Column(String(20), nullable=False)
    fecha_encuesta = Column(TIMESTAMP, server_default=func.now())

    # Sección 1
    navegacion_clara = Column(Integer)
    facil_encontrar_funciones = Column(Integer)
    instrucciones_claras = Column(Integer)
    aprendizaje_rapido = Column(Integer)

    # Sección 2
    tareas_rapidas = Column(Integer)
    pocos_pasos = Column(Integer)
    proceso_citas_agil = Column(Integer)
    registro_eficiente = Column(Integer)

    # Sección 3
    diseño_atractivo = Column(Integer)
    interfaz_amigable = Column(Integer)
    colores_agradables = Column(Integer)
    interfaz_moderna = Column(Integer)

    # Sección 4
    funciones_utiles = Column(Integer)
    cumple_objetivo = Column(Integer)
    satisface_necesidades = Column(Integer)
    recomendaria_uso = Column(Integer)
