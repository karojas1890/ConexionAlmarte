from flask import Blueprint, jsonify, session
from app.models import Consultante,Disponibilidad
from app.models.Disponibilidad import Disponibilidad
from app.models.Servicio import servicios
from app.models.Cita import Citas
from app.extensions import db
from sqlalchemy import func, desc

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/api/pacientes', methods=['GET'])
def VerPacientes():
    try:
        

        pacientes = (
            db.session.query(
        Consultante.identificacion,
        Consultante.nombre,
        Consultante.apellido1,
        Consultante.apellido2,
        Consultante.edad,
        Consultante.correo,
        Consultante.telefono,
        func.max(Citas.citaid).label("ultima_cita_id")
    )
    .outerjoin(Citas, Citas.usuario == Consultante.identificacion)  # fijarse que coincida exactamente
    .group_by(
        Consultante.identificacion,
        Consultante.nombre,
        Consultante.apellido1,
        Consultante.apellido2,
        Consultante.edad,
        Consultante.correo,
        Consultante.telefono
    )
    .all()
)
       
        data = []
        for p in pacientes:
            ultima_cita_str = "Sin cita"
            sesiones_completadas = 0  # temporal, hasta que tengas tabla Sesion

            if p.ultima_cita_id:
        # Obtener la cita
                cita = Citas.query.get(p.ultima_cita_id)
                if cita:
            # Obtener la disponibilidad asociada
                    disponibilidad = Disponibilidad.query.get(cita.iddisponibilidad)
                    if disponibilidad:
                        ultima_cita_str = disponibilidad.fecha.strftime("%d/%m/%Y")
        
            data.append({
        "id": p.identificacion,
        "nombre": f"{p.nombre} {p.apellido1} {p.apellido2 or ''}",
        "edad": p.edad,
        "correo": p.correo,
        "telefono": p.telefono,
        "ultima_cita": ultima_cita_str,
        "sesiones": sesiones_completadas
    })
       
        return jsonify(data)

    except Exception as e:
        print(f"[ERROR]: {e}")
        return jsonify({"error": "No se pudieron cargar los pacientes."}), 500


@pacientes_bp.route('/api/paciente/<identificacion>/historial', methods=['GET'])
def HistorialCitas(identificacion):
    try:
        result = (
            db.session.query(Citas)
            .filter_by(Usuario=identificacion)
            .order_by(desc(Citas.Citaid))
            .limit(10)
            .all()
        )

        data = [
            {
                "id": c.citaid,
                "servicio": c.servicio,
                "disponibilidad": c.iddisponibilidad,
                "estado": (
                    "Pendiente" if c.estado == 0 else
                    "Finalizada" if c.estado == 1 else
                    "Cancelada x Terapeuta" if c.estado == 2 else
                    "Cancelada x Consultante"
                ),
                "pago": "Pendiente" if c.pago == 1 else "Realizado"
            }
            for c in result
        ]
        print(data)
        return jsonify(data), 200

    except Exception as e:
        print(f"[ERROR]: {e}")
        return jsonify({"error": str(e)}), 500
