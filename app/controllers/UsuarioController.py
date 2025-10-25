from flask import Blueprint, request, jsonify, session
from app.extensions import db
from sqlalchemy import text
import random
import string
import bcrypt
from app.Service import email_service 

usuario_bp = Blueprint("Usuarios", __name__, url_prefix="/usuarios")

def GenerarContrasena():
    mayus = random.choice(string.ascii_uppercase)
    minus = random.choice(string.ascii_lowercase)
    num = random.choice(string.digits)
    especial = random.choice("!@#$%^&*()_+")
    resto = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()_+", k=4))
    contrasena = mayus + minus + num + especial + resto
    return ''.join(random.sample(contrasena, len(contrasena)))  # mezclar

def GenerarAlias(nombre, apellido):
    inicial = nombre[0].lower()
    apellido = apellido.split()[0].lower()  
   
    sql = text("""
        SELECT usuario FROM Usuario WHERE usuario LIKE :pattern ORDER BY usuario DESC LIMIT 1
    """)
    pattern = f"{inicial}{apellido}%"
    result = db.session.execute(sql, {"pattern": pattern}).fetchone()
    if result:
        ultimo = int(''.join(filter(str.isdigit, result[0])))  
        nuevo_num = ultimo + 1
    else:
        nuevo_num = 1000
    alias = f"{inicial}{apellido}{nuevo_num}"
    return alias

@usuario_bp.route("/crear", methods=["POST"])
def crearUsuario():
    try:
        data = request.get_json()
        if not data.get("nombre") or not data.get("primerApellido"):
            return jsonify({"error": "Nombre y apellido obligatorios"}), 400

        nombre = data["nombre"]
        apellido = data["primerApellido"]
        correo=data["correo"]
        Uss = GenerarAlias(nombre, apellido)
        contrasena = GenerarContrasena()
        contrasenaHash = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        email_service.SendNewUser(email=correo, username=Uss, password=contrasena)
        
        
        sql = text("SELECT insertUsuario(:usuario, :password, NULL, 1) AS idUsuario")
        result = db.session.execute(sql, {"usuario": Uss, "password": contrasenaHash})


        idUsuario = result.scalar() 
        db.session.commit()

 
        sql_consultante = text("""
            CALL insertConsultante(
                :identificacion,
                :idUsuario,
                :nombre,
                :apellido1,
                :apellido2,
                :telefono,
                :correo,
                :provincia,
                :canton,
                :distrito,
                :direccion,
                :fechaNacimiento,
                :edad,
                :ocupacion,
                :lugarTrabajo,
                :tipo,
                :urlImagen
            )
        """)

        db.session.execute(sql_consultante, {
            "identificacion": data.get("identificacion"),
            "idUsuario": idUsuario,
            "nombre": nombre,
            "apellido1": apellido,
            "apellido2": data.get("segundoApellido"),
            "telefono": data.get("telefono"),
            "correo": data.get("correo"),
            "provincia": data.get("provincia"),
            "canton": data.get("canton"),
            "distrito": data.get("distrito"),
            "direccion": data.get("direccion"),
            "fechaNacimiento": data.get("fechaNacimiento"),
            "edad": data.get("edad"),
            "ocupacion": data.get("ocupacion"),
            "lugarTrabajo": data.get("lugarTrabajo"),
            "tipo": 1,  
            "urlImagen": None
        })
        db.session.commit()
        
        return jsonify({
            "message": "Usuario creado exitosamente"
        }), 201

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": str(e)}), 500
