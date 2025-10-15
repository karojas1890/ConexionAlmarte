from flask import Blueprint, jsonify, session,request
from app.extensions import db
from sqlalchemy import text
from datetime import datetime

perfil_bp = Blueprint('perfil', __name__, url_prefix='/perfil')

@perfil_bp.route("/datos", methods=['GET'])
def ObtenerPerfil():
    try:
        id_usuario = session.get("idusuario")
        if not id_usuario:
            return jsonify({"error": "No hay usuario en sesión"}), 401

        result = db.session.execute(
            text("SELECT * FROM obtenerPerfilPacientePorUsuario(:idusuario)"),
            {"idusuario": id_usuario}
        )

        perfil = [
            {
                "identificacion": row._mapping["identificacion"],
                "nombre": row._mapping["nombre"],
                "apellido1": row._mapping["apellido1"],
                "apellido2": row._mapping["apellido2"],
                "telefono": row._mapping["telefono"],
                "correo": row._mapping["correo"],
                "provincia": row._mapping["provincia"],
                "canton": row._mapping["canton"],
                "distrito": row._mapping["distrito"],
                "direccionexacta": row._mapping["direccionexacta"],
                "fechanacimiento": row._mapping["fechanacimiento"].isoformat() if row._mapping["fechanacimiento"] else None,
                "edad": row._mapping["edad"],
                "ocupacion": row._mapping["ocupacion"],
                "lugartrabajoestudio": row._mapping["lugartrabajoestudio"],
                "urlimagen": row._mapping["urlimagen"]
            }
            for row in result
        ]

        if not perfil:
            return jsonify({"error": "No se encontró el perfil"}), 404
        
        return jsonify(perfil[0]), 200  
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
    

@perfil_bp.route("/guardar", methods=['POST'])
def GuardarPerfil():
    try:
        data = request.get_json()
        print("Datos recibidos:", data)

        # Convertir tipos
        if data.get("fechanacimiento"):
            data["fechanacimiento"] = datetime.strptime(data["fechanacimiento"], "%Y-%m-%d").date()
        else:
            data["fechanacimiento"] = None

        if data.get("edad"):
            data["edad"] = int(data["edad"])
        else:
            data["edad"] = None

        for key in ["direccionexacta", "urlimagen"]:
            if not data.get(key):
                data[key] = None

        sql = text("""
            CALL actualizarperfilpaciente(
                :identificacion,
                :nombre,
                :apellido1,
                :apellido2,
                :telefono,
                :correo,
                :provincia,
                :canton,
                :distrito,
                :direccionexacta,
                :fechanacimiento,
                :edad,
                :ocupacion,
                :lugartrabajoestudio,
                :urlimagen
            )
        """)

        db.session.execute(sql, data)
        db.session.commit()
        
        session["nombre"] = data.get("nombre")
        session["apellido1"] = data.get("apellido1")
        session["correo"] = data.get("correo")
        
        
        return jsonify({"success": True}), 200

    except Exception as e:
        db.session.rollback()
        print("Error al guardar perfil:", e)
        return jsonify({"error": str(e)}), 500