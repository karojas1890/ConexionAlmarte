import requests
from flask import Blueprint, request, jsonify

apiPiscologos_bp = Blueprint("apiP", __name__)

@apiPiscologos_bp.route("/apiP", methods=["POST"])
def VerPsicologos():
    try:

        data_request = request.get_json()

        if not data_request:
            return jsonify({"error": "Debe enviar un JSON con query y searchType"}), 400

        query = data_request.get("query")
        searchType = data_request.get("searchType")

        if not query or not searchType:
            return jsonify({"error": "Faltan parámetros: query y searchType"}), 400

        # Detecta tipo de busqueda
        if searchType == "code":
            url_get = f"https://apipsicologos.onrender.com/api/Psicologos/{query}"
        elif searchType == "name":
            url_get = f"https://apipsicologos.onrender.com/api/Psicologos/nombre/{query}"
        else:
            return jsonify({"error": "searchType debe ser 'code' o 'name'"}), 400

        # Petici0n a el API 
        response = requests.get(url_get)

        if response.status_code == 200:
            data = response.json()

         
            if isinstance(data, list):
                if len(data) == 0:
                    return jsonify({"mensaje": "Sin resultados", "resultado": None}), 200
                data = data[0]  # <- Tomamos solo el primer elemento del arreglo

            return jsonify({
                "mensaje": "Datos recibidos correctamente",
                "resultado": data
            }), 200

        return jsonify({
            "error": "No se encontraron resultados",
            "codigo_http": response.status_code
        }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500
