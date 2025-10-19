from flask import Blueprint, jsonify, session,request,url_for
from app.extensions import db  
from sqlalchemy import text
from app.models import RecomendacionesTerapeuticas,RecomendacionPaciente,RegistroAplicacionRecomendacion,CategoriasRecomendaciones
tools_bp = Blueprint('tools', __name__, url_prefix='/tools')

@tools_bp.route("/recomendaciones_tools", methods=['GET'])
def ObtenerRecomendacionesTools():
    try:
        id_usuario = session.get("idusuario")
        if not id_usuario:
            return jsonify({"error": "No hay usuario en sesión"}), 401

        # lama al SP
        result = db.session.execute(
            text("SELECT * FROM obtenerRecomendacionesPorUsuario(:idusuario)"),
            {"idusuario": id_usuario}
        )

        recomendaciones = []
        for row in result:
            r = RecomendacionPaciente(
                idasignacion=row._mapping["idasignacion"],
                idrecomendacion=row._mapping["idrecomendacion"],
                duraciondias=row._mapping["duraciondias"],
                momento=row._mapping["momento"]
            )

            # relacion del modelo a recomendacion terapautica
            recomendacion = RecomendacionesTerapeuticas(
                nombrerecomendacion=row._mapping["nombrerecomendacion"],
                descripcion=row._mapping["descripcion"],
                urlimagen=row._mapping["urlimagen"]
            )

            categoria_nombre = row._mapping["nombrecategoria"]

            recomendaciones.append({
                "idasignacion": r.idasignacion,
                "idrecomendacion": r.idrecomendacion,
                "nombrerecomendacion": recomendacion.nombrerecomendacion,
                "descripcion": recomendacion.descripcion,
                "urlimagen": url_for('static', filename=f'images/{recomendacion.urlimagen}') if recomendacion.urlimagen else '',               
                "duraciondias": r.duraciondias,
                "momento": r.momento,
                "nombrecategoria": categoria_nombre
            })

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

        # se crea una instancia para  validar el modelo 
        registro = RegistroAplicacionRecomendacion(
            recomendacionaplicada = data.get("idasignacion"),
            efectividad = data.get("efectividad"),
            animoantes = data.get("animoAntes"),
            animodespues = data.get("animoDespues"),
            bienestarantes = data.get("bienestarAntes"),
            bienestardespues = data.get("bienestarDespues"),
            comentario = data.get("comentario")
        )

       

        # ejecuta el SP con los datos del modelo
        sql = text("""
            CALL insertarRegistroHerramienta(
                :p_idUsuario,
                :p_idasignacion,
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
            "p_idasignacion": registro.recomendacionaplicada,
            "p_efectividad": registro.efectividad,
            "p_animoAntes": registro.animoantes,
            "p_animoDespues": registro.animodespues,
            "p_bienestarAntes": registro.bienestarantes,
            "p_bienestarDespues": registro.bienestardespues,
            "p_comentario": registro.comentario
        }

        db.session.execute(sql, params)
        db.session.commit()

        return jsonify({"success": True})

    except Exception as e:
        db.session.rollback()
        print("Error al guardar uso de estrategia:", e)
        return jsonify({"success": False, "error": str(e)})
@tools_bp.route("/Recomendacion/<int:id_asignacion>", methods=['GET'])
def ObtenerRecomendacion(id_asignacion):
    try:
        # Ejecutar la función de PostgreSQL y obtener un diccionario
        sql = text("""
            SELECT * 
            FROM ObtenerRecomendacionPorAsignacion(:idasignacion)
        """)
        result = db.session.execute(sql, {"idasignacion": id_asignacion}).mappings().first()

        if not result:
            return jsonify({"error": "Recomendación no encontrada"}), 404

        # Mapear el resultado
        resultado = {
            "idAsignacion": result["idasignacion"],
            "duracionDias": result["duraciondias"],
            "momento": result["momento"],
            "nombreRecomendacion": result["nombrerecomendacion"],
            "descripcion": result["descripcion"],
            "urlimagen": result["urlimagen"] or '',   # solo el nombre de la imagen
            "duracionMinutos": result["duracionminutos"],
            "categoria": result["nombrecategoria"],
            "descripcionCategoria": result["descripcioncategoria"]
        }

        return jsonify(resultado)

    except Exception as e:
        db.session.rollback()
        print("Error al obtener recomendación:", e)
        return jsonify({"error": str(e)}), 500


@tools_bp.route("/HistorialHerramientas", methods=['GET'])
def ObtenerHistorialHerramientas():
    try:
        id_usuario = session.get("idusuario")
        if not id_usuario:
            return jsonify({"error": "Usuario no logueado"}), 401

        # Llamamos a la función SQL
        sql = text("SELECT * FROM obtenerRegistrosAplicacion(:p_idusuario)")
        result = db.session.execute(sql, {"p_idusuario": id_usuario})

        registros = []
        for row in result:
            registros.append({
                "idregistro": row._mapping["idregistro"],
                "idasignacion": row._mapping["idasignacion"],  # 🔹 aquí usamos el nombre correcto
                "efectividad": row._mapping["efectividad"],
                "animoantes": row._mapping["animoantes"],
                "animodespues": row._mapping["animodespues"],
                "bienestarantes": row._mapping["bienestarantes"],
                "bienestardespues": row._mapping["bienestardespues"],
                "comentario": row._mapping["comentario"],
                "fechahoraregistro": row._mapping["fechahoraregistro"].strftime("%Y-%m-%d %H:%M:%S"),
                "nombrerecomendacion": row._mapping["nombrerecomendacion"],
                "nombrecategoria": row._mapping["nombrecategoria"]
            })

        return jsonify(registros), 200

    except Exception as e:
        print("Error al obtener historial de herramientas:", e)
        return jsonify({"error": str(e)}), 500

