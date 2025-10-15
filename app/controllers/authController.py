from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import Usuario
from sqlalchemy import text
from app import db

auth_bp = Blueprint("auth", __name__)

#login es el endopoint que vamos a usar en login por ejemplo apra llamar esta funcion


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        # Ejecutar el SP
        sql = text("SELECT * FROM loginUsuario(:usuario, :password);")
        result = db.session.execute(sql, {"usuario": usuario, "password": password})
        user_data = result.fetchone()  

        if user_data is None:
            flash("Usuario o contraseña inválidos", "error")
            return redirect(url_for("auth.login"))

        # Limpia sesion anterior
        session.clear()

        # Guardara datos en sesion
        session["idusuario"] = user_data.idusuario
        session["usuario"] = usuario
        session["rol"] = user_data.tipo
        session["nombre"] = user_data.nombre
        session["apellido1"] = user_data.apellido1
        session["correo"]=user_data.correo
        session["idterapeuta"]=user_data.identificacion_terapeuta
        # Si el usuario es consultante, guarda también datos del terapeuta
        if user_data.tipo == 1:  # 1 = Consultante
            
            session["terapeuta_nombre"] = user_data.terapeuta_nombre
            session["terapeuta_apellido1"] = user_data.terapeuta_apellido1
            session["terapeuta_apellido2"] = user_data.terapeuta_apellido2
            session["terapeuta_codigoProfesional"] = user_data.terapeuta_codigoprofesional

       

        return redirect(url_for("routes.verificar_Codigo"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
