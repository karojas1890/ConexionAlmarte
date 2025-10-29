from flask import Blueprint, request, jsonify,url_for,session
from app.extensions import db
from app.models.Disponibilidad import Disponibilidad
from app.models.Servicio import servicios
from sqlalchemy import text
from app.Service import email_service
from app.Service.auditoria import registrarAuditoria
   
citas_bp = Blueprint("Citas", __name__,url_prefix='/citas')


@citas_bp.route("/citas", methods=["POST"])
def CrearCita():
    try:
        data = request.get_json()
        print(data)

        # Valida  campos 
        if not data.get("usuario") or not data.get("servicio") or not data.get("iddisponibilidad"):
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        #  valores por defecto
        estado = data.get("estado", 0)
        pago = data.get("pago", 1)

        # Eejecuta el procedimiento almacenado
        sql = text("""
            CALL insertarCita(
                :usuario,
                :servicio,
                :iddisponibilidad,
                :pago,
                :estado
            )
        """)
        db.session.execute(sql, {
            "usuario": data["usuario"],
            "servicio": data["servicio"],
            "iddisponibilidad": data["iddisponibilidad"],
            "pago": pago,
            "estado": estado
        })
        db.session.commit()
        
        disponibilidad = db.session.query(Disponibilidad).filter_by(
            iddisponibilidad=data["iddisponibilidad"]
        ).first()

        
        servicio = db.session.query(servicios).filter_by(
            idservicio=data["servicio"]
        ).first()
        
        if not disponibilidad:
            return jsonify({"message": "Cita creada, pero no se encontró la disponibilidad."}), 201
        
        if not servicio:
            return jsonify({"message": "Servicio no encontrado."}), 404

        nombreservicio = servicio.nombreservicio
        
        correo = session.get("correo_terapeuta")  
        paciente = session.get("nombre")  
        fecha = f"{disponibilidad.fecha} de {disponibilidad.horainicio} a {disponibilidad.horafin}"
        
        
        terapeuta = disponibilidad.terapeuta_rel
        if not terapeuta:
            return jsonify({"message": "Cita creada, pero no se encontró el terapeuta asociado."}), 201

       
        email_service.SendNewAppointment(
                mail=correo ,
                pacient=paciente,
                date=fecha,
                nombreServicio=nombreservicio
            )
        cp=session.get("correo")
        terapeuta=session.get("terapeuta_nombre")
        apellido=session.get("terapeuta_apellido1")
        email_service.SendNewAppointmentPacient(
                mail=cp ,
                pacient=paciente,
                date=fecha,
                nombreServicio=nombreservicio,
                nombreTerapeuta=terapeuta +" "+apellido
            )
        registrarAuditoria(
            identificacion_consultante=data["usuario"],
            tipo_actividad=2,  
            descripcion=f"Cita reservada",
            datos_modificados={"servicio": data["servicio"], "hora": fecha},
            exito=True
            )
        return jsonify({
            "message": "Cita creada exitosamente",
            "cita": {
                "usuario": data["usuario"],
                "servicio": data["servicio"],
                "iddisponibilidad": data["iddisponibilidad"],
                "estado": estado,
                "pago": pago
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        
        return jsonify({"error": str(e)}), 500
    
    
    
@citas_bp.route('/disponibilidad', methods=['GET'])
def ObtenerDisponibilidad():
    try:
        result = db.session.execute(text("SELECT * FROM ObtenerDisponibilidades()"))

        data = [
            {
               "id": row.iddisponibilidad,
               "fecha": row.fecha.strftime("%Y-%m-%d"),
               "hora_inicio": row.horainicio.strftime("%H:%M"),
               "hora_fin": row.horafin.strftime("%H:%M"),
               "estado": row.estado,
              "id_terapeuta": row.idterapeuta,
            }
               for row in result
               if row.estado == 1
        ]
     
        return jsonify(data)

    except Exception as e:
        
        
        return jsonify({"error": str(e)}), 500
    
@citas_bp.route("/servicios", methods=['GET'])
def Servicios():
    try:
   
        result = db.session.execute(text("SELECT * FROM ObtenerServicios()"))
        
        
        servicios = [
            {
                "idservicio": row.idservicio,
                "nombreservicio": row.nombreservicio,
                "descripcionservicio": row.descripcionservicio,
                "urlimagen": url_for('static', filename=f'images/{row.urlimagen}') if row.urlimagen else '',
                "duracionHoras": row.duracionhoras,
                "precio": float(row.precio) if row.precio is not None else None
            }
            for row in result
        ]

        return jsonify(servicios)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

@citas_bp.route("/pendientes", methods=['GET'])
def CitasPendientes():
    try:
        
        id_usuario = session.get("idusuario")
        if not id_usuario:
            return jsonify({"error": "No hay usuario en sesión"}), 401

     
        query = text("SELECT * FROM obtenerCitasUsuario(:usuario)")
        result = db.session.execute(query, {"usuario": id_usuario})

        
        citas = [
            {
                "nombreservicio": row._mapping["nombreservicio"],
                "fecha": row._mapping["fecha"].isoformat() if row._mapping["fecha"] else None,
                "horainicio": row._mapping["horainicio"].strftime("%H:%M") if row._mapping["horainicio"] else None,
                "nombre_terapeuta": row._mapping["nombre_terapeuta"],
                "apellido1_terapeuta": row._mapping["apellido1_terapeuta"],
                "apellido2_terapeuta": row._mapping["apellido2_terapeuta"],
                "estado": row._mapping.get("estado")
            }
            for row in result
        ]

      
        return jsonify(citas), 200

    except Exception as e:
       
        return jsonify({"error": str(e)}), 500