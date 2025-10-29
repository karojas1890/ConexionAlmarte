from flask import Blueprint, jsonify
from app.models import Auditoria

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
