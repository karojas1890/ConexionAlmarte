from flask import Flask
from app.extensions import db
import os

from app.models import (
    Usuario, Consultante, PME, Terapeuta, Servicio, Disponibilidad,
    Cita, MetodoPago, PagoCita, CategoriaRecomendacion,
    RecomendacionTerapeutica, RecomendacionPaciente,
    RegistroAplicacionRecomendacion, RecursoApoyo, Emocion,
    ConductaAfrontamiento, Diario, Tarjeta,Auditoria,RestriccionPassword,Pais,CiudadMunicipio,LocalidadBarrio,EstadoProvincia
)

from app.Service import email_service,smsservice  



# Genera la clave


def create_app():
    app = Flask(__name__)

    #  Configuración de base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql://almarte:rfBfAn8FgBijU1U9k6GJVzgNepBxmrUt@dpg-d3m2mt8gjchc73cr1m1g-a.oregon-postgres.render.com/conexion_almarte"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #  Clave secreta para sesiones
    app.secret_key = os.getenv(
        "SECRET_KEY",
        "9a8c7e4f1d2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d"
    )

    #  Inicializa la base de datos
    db.init_app(app)

    # Seguridad de cookies
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    #  Configuración del servicio de correo
    
    email_service.init_app(app) 
    smsservice.init_app(app) 

   

    #  Registra los blueprints
    from .controllers.citaController import citas_bp
    from .controllers.routes import routes_bp
    from .controllers.authController import auth_bp
    from .controllers.diaryController import diary_bp
    from .controllers.toolsController import tools_bp
    from .controllers.perfilController import perfil_bp
    from .controllers.disponibilidadController import availability_bp
    from .controllers.UsuarioController import usuario_bp
    from .controllers.credentialController import credential_bp 
    from .controllers.tarjetasController import card_bp
    from .controllers.pacientesController import pacientes_bp 
    from .controllers.auditoriaController import auditoria_bp
    from .controllers.GetGeolocalizacion import geolocalizacion_bp
    from .controllers.APIPsicologos import apiPiscologos_bp
    
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(citas_bp)
    app.register_blueprint(diary_bp)
    app.register_blueprint(tools_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(availability_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(credential_bp)
    app.register_blueprint(card_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(auditoria_bp)
    app.register_blueprint(geolocalizacion_bp)
    app.register_blueprint(apiPiscologos_bp)
    return app
