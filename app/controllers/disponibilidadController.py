from flask import Blueprint, jsonify, session, request
from app.extensions import db  
from sqlalchemy import text,and_
from datetime import datetime
from app.models import Disponibilidad


availability_bp = Blueprint('availability', __name__, url_prefix='/availability')


@availability_bp.route("/AgregarDisponibilidad", methods=['POST'])
def AgregarDisponibilidad():
    try:
        data = request.get_json()
        slots = data.get("slots", [])

        
        id_terapeuta = "304450927"

        if not slots:
            return jsonify({"error": "No se enviaron slots"}), 400

        for slot in slots:
          
            try:
                fecha = datetime.strptime(slot["fecha"], "%Y-%m-%d").date()
                hora_inicio = datetime.strptime(slot["hora_inicio"], "%H:%M").time()
                hora_fin = datetime.strptime(slot["hora_fin"], "%H:%M").time()
            except Exception:
                return jsonify({"error": f"Formato incorrecto en el slot: {slot}"}), 400

            if hora_fin <= hora_inicio:
                return jsonify({"error": f"La hora de fin debe ser mayor que la hora de inicio: {slot}"}), 400

          
            db.session.execute(
                text("CALL RegistrarDisponibilidad(:fecha, :horainicio, :horafin, :idterapeuta)"),
                {
                    "fecha": fecha,
                    "horainicio": hora_inicio,
                    "horafin": hora_fin,
                    "idterapeuta": id_terapeuta
                }
            )

        db.session.commit()
        return jsonify({"msg": "Disponibilidades registradas exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        print("Error al agregar disponibilidad:", e)
        return jsonify({"error": str(e)}), 500