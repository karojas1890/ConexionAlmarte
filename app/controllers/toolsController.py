from flask import Blueprint, jsonify, session,request
from app.extensions import db  
from sqlalchemy import text
tools_bp = Blueprint('tools', __name__, url_prefix='/tools')

@tools_bp.route("/recomendaciones_tools", methods=['GET'])
def ObtenerRecomendacionesTools():
    try:
        id_usuario = session.get("idusuario")
        if not id_usuario:
            return jsonify({"error": "No hay usuario en sesión"}), 401

        result = db.session.execute(
            text("SELECT * FROM obtenerRecomendacionesPorUsuario(:idusuario)"),
            {"idusuario": id_usuario}
        )

        recomendaciones = [
            {
                "idasignacion": row._mapping["idasignacion"],
                "nombrerecomendacion": row._mapping["nombrerecomendacion"],
                "descripcion": row._mapping["descripcion"],
                "urlimagen": row._mapping["urlimagen"],
                "duraciondias": row._mapping["duraciondias"],
                "momento": row._mapping["momento"],
                "nombrecategoria": row._mapping["nombrecategoria"]
            }
            for row in result
        ]

        return jsonify(recomendaciones), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tools_bp.route("/GuardarUso", methods=['POST'])
def GuardarUso():
    try:
        data = request.get_json()
        id_usuario = session.get("idusuario")

        if not id_usuario:
            return jsonify({"success": False, "error": "Usuario no logueado"}), 401

    
        sql = text("""
            CALL insertarRegistroHerramienta(
                :p_idUsuario,
                :p_recomendacionAplicada,
                :p_efectividad,
                :p_animoAntes,
                :p_animoDespues,
                :p_bienestarAntes,
                :p_bienestarDespues,
                :p_comentario
            )
        """)

        params = {
            "p_idUsuario": id_usuario,
            "p_recomendacionAplicada": data.get("recomendacionAplicada"),
            "p_efectividad": data.get("efectividad"),
            "p_animoAntes": data.get("animoAntes"),
            "p_animoDespues": data.get("animoDespues"),
            "p_bienestarAntes": data.get("bienestarAntes"),
            "p_bienestarDespues": data.get("bienestarDespues"),
            "p_comentario": data.get("comentario")
        }

        db.session.execute(sql, params)
        db.session.commit()

        return jsonify({"success": True})

    except Exception as e:
        db.session.rollback()
        print("Error al guardar uso de estrategia:", e)
        return jsonify({"success": False, "error": str(e)})
