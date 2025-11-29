from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.encuesta import EncuestaUsabilidad

encuesta_bp = Blueprint("encuesta", __name__)

@encuesta_bp.route("/encuesta", methods=["POST"])
def GuardarEncuesta():
    try:
        datos = request.get_json()

        usuario_id = datos.get("usuario_id")
        rol_usuario = datos.get("rol_usuario")

        if not usuario_id or not rol_usuario:
            return jsonify({"error": "usuario_id y rol_usuario son obligatorios"}), 400

        encuesta = EncuestaUsabilidad(
            usuario_id=usuario_id,
            rol_usuario=rol_usuario,
            navegacion_clara=datos.get("navegacion_clara"),
            facil_encontrar_funciones=datos.get("facil_encontrar_funciones"),
            instrucciones_claras=datos.get("instrucciones_claras"),
            aprendizaje_rapido=datos.get("aprendizaje_rapido"),
            tareas_rapidas=datos.get("tareas_rapidas"),
            pocos_pasos=datos.get("pocos_pasos"),
            proceso_citas_agil=datos.get("proceso_citas_agil"),
            registro_eficiente=datos.get("registro_eficiente"),
            diseño_atractivo=datos.get("diseño_atractivo"),
            interfaz_amigable=datos.get("interfaz_amigable"),
            colores_agradables=datos.get("colores_agradables"),
            interfaz_moderna=datos.get("interfaz_moderna"),
            funciones_utiles=datos.get("funciones_utiles"),
            cumple_objetivo=datos.get("cumple_objetivo"),
            satisface_necesidades=datos.get("satisface_necesidades"),
            recomendaria_uso=datos.get("recomendaria_uso"),
        )

        db.session.add(encuesta)
        db.session.commit()

        return jsonify({"mensaje": "Encuesta guardada exitosamente"}), 201

    except Exception as e:
        print("ERROR GuardarEncuesta:", e)
        return jsonify({"error": "Error al guardar la encuesta"}), 500
@encuesta_bp.route("/encuesta", methods=["GET"])
def VerEncuesta():
    try:
        encuestas = EncuestaUsabilidad.query.all()

        data = [
            {
                "id": e.id,
                "usuario_id": e.usuario_id,
                "rol_usuario": e.rol_usuario,
                "fecha_encuesta": e.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
                "navegacion_clara": e.navegacion_clara,
                "facil_encontrar_funciones": e.facil_encontrar_funciones,
                "instrucciones_claras": e.instrucciones_claras,
                "aprendizaje_rapido": e.aprendizaje_rapido,
                "tareas_rapidas": e.tareas_rapidas,
                "pocos_pasos": e.pocos_pasos,
                "proceso_citas_agil": e.proceso_citas_agil,
                "registro_eficiente": e.registro_eficiente,
                "diseño_atractivo": e.diseño_atractivo,
                "interfaz_amigable": e.interfaz_amigable,
                "colores_agradables": e.colores_agradables,
                "interfaz_moderna": e.interfaz_moderna,
                "funciones_utiles": e.funciones_utiles,
                "cumple_objetivo": e.cumple_objetivo,
                "satisface_necesidades": e.satisface_necesidades,
                "recomendaria_uso": e.recomendaria_uso
            }
            for e in encuestas
        ]

        return jsonify(data), 200

    except Exception as e:
        print("ERROR VerEncuesta:", e)
        return jsonify({"error": "No se pudieron obtener las encuestas"}), 500
