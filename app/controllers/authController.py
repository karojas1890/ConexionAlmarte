from flask import Blueprint, render_template, request, redirect, url_for, session, flash,current_app,jsonify
from sqlalchemy import text
from app import db
import bcrypt
import random
from app.Service import smsservice
from app.Service.auditoria import registrarAuditoria
from datetime import datetime,timedelta
import threading

auth_bp = Blueprint("auth", __name__)



@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        
        
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        # Valida usuario y obtener hash de la contraseña
        sql_user = text("SELECT idusuario, password, intentos, estado, tipo FROM usuario WHERE usuario=:usuario")
        result_user = db.session.execute(sql_user, {"usuario": usuario})
        user = result_user.fetchone()

        if not user:
            flash("Usuario o password incorrecto inténtelo de nuevo")
            return redirect(url_for("auth.login"))

        if user.estado != 1:
            flash("Usuario bloqueado. Restablezca la contraseña.", "error")
            return redirect(url_for("auth.login"))

        #  Verifica contrasena con bcrypt
        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            session["usuarioLog"] = user.idusuario
            # Obtener teléfono según tipo
            if user.tipo in (1, 3, 4):  # Consultante
               sql_tel = text("SELECT telefono FROM consultante WHERE idusuario = :idusuario")
            elif user.tipo == 2:  # Terapeuta
                sql_tel = text("SELECT telefono FROM terapeuta WHERE idusuario = :idusuario")
            else:
                sql_tel = None

            telefono = None
            if sql_tel is not None:
               result_tel = db.session.execute(sql_tel, {"idusuario": user.idusuario})
               telefono = result_tel.scalar()
    
            session["phoneLog"] = telefono
            # Incrementar intentos
            intentos = user.intentos + 1
            estado = 0 if intentos >= 3 else 1
            sql_update = text("UPDATE usuario SET intentos=:intentos, estado=:estado WHERE idusuario=:idusuario")
            db.session.execute(sql_update, {"intentos": intentos, "estado": estado, "idusuario": user.idusuario})
            db.session.commit()
            
            if estado == 0:
                flash("Usuario bloqueado por demasiados intentos fallidos. Restablezca la contraseña", "error")
                registrarAuditoria(
            identificacion_consultante=session.get("usuarioLog"),
            tipo_actividad=12,
            descripcion="Bloqueo por ecxeso de intentos", 
             exito=False
            )
#            smsservice.BloqueoCuenta(telefono)
            else:
                flash("Usuario o password incorrecto inténtelo de nuevo")
                registrarAuditoria(
            identificacion_consultante=session.get("usuarioLog"),
            tipo_actividad=11,
            descripcion="Error de Login",
             exito=False
            )
            
            return redirect(url_for("auth.login"))

        # si la contrasena es correcta  resetea intentos
        sql_reset = text("UPDATE usuario SET intentos=0 WHERE idusuario=:idusuario")
        db.session.execute(sql_reset, {"idusuario": user.idusuario})
        db.session.commit()

        #  limpia la sesion previa
        session.clear()

        
        sql_func = text("SELECT * FROM loginUsuario(:usuario)")
        result_func = db.session.execute(sql_func, {"usuario": usuario})
        user_data = result_func.fetchone()

        if not user_data:
            flash("Error al cargar datos del usuario", "error")
            return redirect(url_for("auth.login"))

        # Guardar datos en sesión
        session["idusuario"] = user_data.idusuario
        session["usuario"] = usuario
        session["rol"] = user_data.tipo
        session["nombre"] = user_data.nombre
        session["apellido1"] = user_data.apellido1
        session["correo"] = user_data.correo
        session["idterapeuta"] = user_data.identificacion_terapeuta
      
        if user_data.tipo in {1,3,4}:  # Consultante
            session["correo_terapeuta"] = user_data.correo_terapeuta
            session["terapeuta_nombre"] = user_data.terapeuta_nombre
            session["terapeuta_apellido1"] = user_data.terapeuta_apellido1
            session["terapeuta_apellido2"] = user_data.terapeuta_apellido2
            session["terapeuta_codigoProfesional"] = user_data.terapeuta_codigoprofesional
            correo = session.get("correo") 
        elif user_data.tipo==2:
            session["correo_terapeuta"] = user_data.correo_terapeuta
            correo = session.get("correo_terapeuta") 
               
        
        idusuario = session.get("idusuario")
        registrarAuditoria(
            identificacion_consultante=idusuario,
            tipo_actividad=7,
            descripcion="Login exitoso",
            exito=True
            )
        nombre = session.get("nombre")
        app = current_app._get_current_object()
        threading.Thread(target=SendCode, args=(app,idusuario, correo, nombre)).start()
        
        return redirect(url_for("routes.verificar_Codigo"))
    
    return render_template("login.html")

@auth_bp.route('/reenviar_codigo', methods=['POST'])
def ReenviarCodigo():
    try:
        # Verificar que existan los datos en sesión
        idusuario = session.get("idusuario")
        correo = session.get("correo")
        nombre = session.get("nombre")
        
        if not all([idusuario, correo, nombre]):
            return jsonify({'success': False, 'message': 'Sesión expirada'}), 400
        
      
        app = current_app._get_current_object()
        
        
        threading.Thread(
            target=SendCode, 
            args=(app, idusuario, correo, nombre),
            daemon=True  
        ).start()
        
        # Responder inmediatamente al frontend
        return jsonify({
            'success': True, 
            'message': 'Código reenviado exitosamente'
        })
        
    except Exception as e:
     
        return jsonify({
            'success': False, 
            'message': 'Error al reenviar el código'
        }), 500

def GenerarCodigo():
    return "{:06d}".format(random.randint(0, 999999))



def SendCode(app,idusuario, correo, nombre):
    from app import db
    from app.Service import email_service
    with app.app_context():
       code = GenerarCodigo()

       sql_update = text("""
        UPDATE usuario 
        SET codigo6digitos=:codigo, codigo_expiracion=:exp
        WHERE idusuario=:idusuario
    """)

       expiracion = datetime.utcnow() + timedelta(seconds=60)
       db.session.execute(sql_update, {"codigo": code, "exp": expiracion, "idusuario": idusuario})
       db.session.commit()

       email_service.SendVerificationCode(email=correo, username=nombre, code=code)

@auth_bp.route("/verificar_codigo", methods=["GET", "POST"])
def VerificarCodigo():
    if request.method == "POST":
        codigo_ingresado = request.form.get("codigo")
        sql = text("""
            SELECT codigo6digitos, codigo_expiracion 
            FROM usuario 
            WHERE idusuario=:idusuario
        """)
        result = db.session.execute(sql, {"idusuario": session["idusuario"]}).fetchone()
        
        if not result:
            flash("Error interno", "error")
            return redirect(url_for("routes.verificar_Codigo"))
        
        if datetime.utcnow() > result.codigo_expiracion:
            flash("El código ha expirado", "error")
            return redirect(url_for("auth.login"))
        
        if codigo_ingresado != result.codigo6digitos:
            flash("Código incorrecto", "error")
            return redirect(url_for("routes.verificar_Codigo"))
        
        
        sql_reset = text("UPDATE usuario SET codigo6digitos=NULL, codigo_expiracion=NULL WHERE idusuario=:idusuario")
        db.session.execute(sql_reset, {"idusuario": session["idusuario"]})
        db.session.commit()
        rol=session.get("rol")
        if rol==1:
            return redirect(url_for("routes.dashboard_Consultante"))
        elif rol==2:
            return redirect(url_for("routes.dashboard"))
        elif  rol in [3, 4]:
            return url_for("routes.quien_eres")
    return render_template("verificar_codigo.html")
   
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
