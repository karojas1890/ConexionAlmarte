from flask import Blueprint, jsonify, session, request
from app.extensions import db  
from sqlalchemy import text,and_
from datetime import datetime
from app.models import Disponibilidad


availability_bp = Blueprint('availability', __name__, url_prefix='/availability')


@availability_bp.route("/disponibilidad", methods=['POST'])
def AgregarDisponibilidad():
    try:
        data = request.get_json()
        slots = data.get("slots", [])
        id_terapeuta = session.get("id_terapeuta")  # variable de sesión

        if not id_terapeuta:
            return jsonify({"error": "Terapeuta no identificado en sesión"}), 401

        for slot in slots:
            # Validar formatos
            try:
                fecha = datetime.strptime(slot["fecha"], "%Y-%m-%d").date()
                hora_inicio = datetime.strptime(slot["hora_inicio"], "%H:%M").time()
                hora_fin = datetime.strptime(slot["hora_fin"], "%H:%M").time()
            except Exception:
                return jsonify({"error": f"Formato incorrecto para el slot: {slot}"}), 400

            # Validar que hora_fin > hora_inicio
            if hora_fin <= hora_inicio:
                return jsonify({"error": f"Hora de fin debe ser mayor que hora de inicio: {slot}"}), 400

            # Verificaa si hay conflictos con la BD
            conflicto = db.session.query(Disponibilidad).filter(
                Disponibilidad.idterapeuta == id_terapeuta,
                Disponibilidad.fecha == fecha,
                Disponibilidad.estado == 1,
                and_(
                    Disponibilidad.horainicio < hora_fin,
                    Disponibilidad.horafin > hora_inicio
                )
            ).first()

            if conflicto:
                return jsonify({"error": f"Conflicto con disponibilidad existente: {slot}"}), 409

            # Si pasa validaciones, llamar al SP
            sql = text("SELECT RegistrarDisponibilidad(:fecha, :horainicio, :horafin, :id_terapeuta)")
            db.session.execute(sql, {
                "fecha": fecha,
                "horainicio": hora_inicio,
                "horafin": hora_fin,
                "id_terapeuta": id_terapeuta
            })

        db.session.commit()
        return jsonify({"msg": "Disponibilidades registradas"}), 200

    except Exception as e:
        db.session.rollback()
        print("Error al agregar disponibilidad:", e)
        return jsonify({"error": str(e)}), 500