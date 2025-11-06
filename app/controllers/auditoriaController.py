from flask import Blueprint, jsonify,session
from app.models import Auditoria
from app import db

auditoria_bp = Blueprint("auditoria", __name__)

@auditoria_bp.route("/auditorias", methods=["GET"])
def ObtenerAuditorias():
    try:
        registros = Auditoria.query.order_by(Auditoria.fecha.desc()).all()

        data = []
        for row in registros:
            data.append({
                "id_actividad": row.id_actividad,
                "identificacion_consultante": row.identificacion_consultante,
                "tipo_actividad": row.tipo_actividad,
                "descripcion": row.descripcion,
                "codigo": row.codigo,
                "fecha": row.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "ip_origen": row.ip_origen,
                "dispositivo": row.dispositivo,
                "ubicacion": row.ubicacion,
                "datos_modificados": row.datos_modificados,
                "exito": row.exito
            })

        return jsonify(data)
    except Exception as e:
        print(f"[ERROR AUDITORIA]: {e}")
        return jsonify({"error": str(e)}), 500
    
@auditoria_bp.route("/auditoria_Uss", methods=["GET"])
def ObtenerAuditoriaUsuario():
    try:
        user_id = session.get("idusuario")
        if not user_id:
            return jsonify({"error": "Usuario no autenticado"}), 401

        # Llama a la funcion SQL en PostgreSQL
        query = "SELECT * FROM obtener_auditoria_usuario(:id)"
        result = db.session.execute(db.text(query), {"id": str(user_id)}).mappings().all()

        # Convierte el resultados a lista de diccionarios
        auditoria_data = [dict(row) for row in result]

        return jsonify({"data": auditoria_data}), 200

    except Exception as e:
        print("Error obteniendo auditoría:", str(e))
        return jsonify({"error": "Error al obtener datos de auditoría"}), 500
