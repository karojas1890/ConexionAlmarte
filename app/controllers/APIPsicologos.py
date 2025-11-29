from flask import Blueprint, jsonify, request
from app.models import ProfesionalPsicologia


apiPiscologos_bp = Blueprint("apiP", __name__)
@apiPiscologos_bp.route("/apiP", methods=["POST"])
def VerPsicologos():
    try:
        datos = request.get_json()

        codigo = datos.get("code")
        nombre = datos.get("name")

        print(f"Codigo {codigo}, nombre {nombre}")

        # Validacion
        if not codigo and not nombre:
            return jsonify({
                "error": "Debe enviar 'code' o 'name' para realizar la búsqueda."
            }), 400

       
        if codigo:
            psicologo = ProfesionalPsicologia.query.get(codigo)

            if not psicologo:
                return jsonify({"error": "Psicólogo no encontrado"}), 404

            data = {
                "codigoprofesional": psicologo.codigoprofesional,
                "nombre": psicologo.nombre,
                "apellido1": psicologo.apellido1,
                "apellido2": psicologo.apellido2,
                "estadoresponsabilidadeconomica": psicologo.estadoresponsabilidadeconomica,
                "estado": psicologo.estado,
                "habilitacionesevaluaciones": psicologo.habilitacionesevaluaciones,
                "areatrabajo": psicologo.areatrabajo,
                }

            return jsonify({"resultado": data}), 200

        
        if nombre:
            psicologos = ProfesionalPsicologia.query.filter_by(nombre=nombre).all()

            if not psicologos:
                  return jsonify({"error": "No se encontraron psicólogos con ese nombre"}), 404

            lista = [
            {
                 "codigoprofesional": p.codigoprofesional,
                "nombre": p.nombre,
                "apellido1": p.apellido1,
                "apellido2": p.apellido2,
                "estadoresponsabilidadeconomica": p.estadoresponsabilidadeconomica,
                "estado": p.estado,
                "habilitacionesevaluaciones": p.habilitacionesevaluaciones,
                "areatrabajo": p.areatrabajo,
            }
              for p in psicologos
            ]

            return jsonify({"resultado": lista}), 200


    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Error en el servidor"}), 500