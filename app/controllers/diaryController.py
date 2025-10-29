from flask import Blueprint, jsonify, session, request
from app.extensions import db  
from sqlalchemy import text
from app.Service.auditoria import registrarAuditoria
from  datetime import datetime
diary_bp = Blueprint('diary', __name__, url_prefix='/diary')


@diary_bp.route("/emociones", methods=['GET'])
def ObtenerEmociones():
    try:
        result = db.session.execute(text("SELECT * FROM obteneremociones()"))
        emociones = [
            {
                "id": row._mapping["id"],
                "nombre": row._mapping["nombre"],
                "descripcion": row._mapping["descripcion"]
            }
            for row in result
        ]
        return jsonify(emociones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@diary_bp.route("/afrontamiento", methods=['GET'])
def ObtenerAfrontamiento():
    try:
        result = db.session.execute(text("SELECT * FROM obtenerafrontamiento()"))
        conductas = [
            {
                "id": row._mapping["id"],
                "nombre": row._mapping["nombre_conducta"],
                "descripcion": row._mapping["descripcion_conducta"]
            }
            for row in result
        ]
       
        return jsonify(conductas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@diary_bp.route("/diario", methods=['GET'])
def ObtenerDiario():
    try:
        id_usuario = session.get("idusuario")
        if not id_usuario:
            return jsonify({"error": "No hay usuario en sesión"}), 401

        # Llamar la función en PostgreSQL
        result = db.session.execute(
            text("SELECT * FROM obtenerdiariocondetallesporusuario(:idusuario)"),
            {"idusuario": id_usuario}
        )

        registros = [dict(row._mapping) for row in result]

        
        avances = [r for r in registros if r["tiporegistro"] == 1]
        disparadores = [r for r in registros if r["tiporegistro"] == 0]

        return jsonify({
            "avances": avances,
            "disparadores": disparadores
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@diary_bp.route("/recomendaciones", methods=['GET'])
def ObtenerRecomendaciones():
    try:
        id_usuario = session.get("idusuario")
        if not id_usuario:
            return jsonify({"error": "No hay usuario en sesión"}), 401

        result = db.session.execute(
            text("SELECT * FROM obtenerrecomendacionesdiario(:idusuario)"),
            {"idusuario": id_usuario}
        )

        recomendaciones = [
            {
                "idasignacion": row._mapping["idasignacion"],
                "idrecomendacion": row._mapping["idrecomendacion"],
                "nombre": row._mapping["nombre"],
                "descripcion": row._mapping["descripcion"],
                "urlimagen": row._mapping["urlimagen"],
                "duracionminutos": row._mapping["duracionminutos"],
                "duraciondias": row._mapping["duraciondias"],
                "momento": row._mapping["momento"]
            }
            for row in result
        ]

        return jsonify(recomendaciones), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@diary_bp.route("/guardar_evento", methods=["POST"])
def GuardarEvento():
    try:
        data = request.get_json()
        print("Datos recibidos:", data)

        # Validar datos mínimos
        if not data.get("situacion") or not data.get("emocion_id") or not data.get("afrontamiento_id") or not data.get("estrategia_id"):
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        # Ejecuta el sp
        sql = text("""
            CALL insertarDiario(
                :p_idusuario,
                :p_tiporegistro,
                :p_descripcion,
                :p_emocion,
                :p_conducta,
                :p_idrecomendacion,
                :p_efectividad
            )
        """)

        db.session.execute(sql, {
            "p_idusuario": session.get("idusuario"),
            "p_tiporegistro": data.get("tiporegistro", 0),
            "p_descripcion": data["situacion"],
            "p_emocion": data["emocion_id"],
            "p_conducta": data["afrontamiento_id"],
            "p_idrecomendacion": data["estrategia_id"],
            "p_efectividad": int(data.get("efectividad", 0))
        })
        db.session.commit()
        registrarAuditoria(
            identificacion_consultante=session.get("idusuario"),
            tipo_actividad=4,  
            descripcion="Registro de Diario",
            datos_modificados = { "servicio": data.get("tiporegistro", 0),"hora": datetime.now()},
            exito=True
        )
        return jsonify({"mensaje": "Registro guardado exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        print("Error al guardar evento:", e)
        return jsonify({"error": str(e)}), 500
