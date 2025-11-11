from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.pais import Pais
from app.models.Estado_Provincia import EstadoProvincia
from app.models.Ciudad_Municipio import CiudadMunicipio
from app.models.Localidad_Barrio import LocalidadBarrio

geolocalizacion_bp = Blueprint("geolocalizacion", __name__)


@geolocalizacion_bp.route("/paises", methods=["GET"])
def GetPais():
    try:
        paises = Pais.query.filter_by(activo=True).all()
        data = [
            {
                "id": p.id,
                "nombre": p.nombre,
                "codigo_iso": p.codigo_iso,
                "fecha_creacion": p.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for p in paises
        ]
        return jsonify(data)
    except Exception as e:
        print(f"[ERROR get_paises]: {e}")
        return jsonify({"error": "No se pudieron obtener los países"}), 500



@geolocalizacion_bp.route("/estados", methods=["GET"])
def GetEstado():
    try:
        pais_id = request.args.get("pais_id", type=int)
        if not pais_id:
            return jsonify({"error": "Se requiere el parámetro 'pais_id'"}), 400

        estados = EstadoProvincia.query.filter_by(pais_id=pais_id, activo=True).all()
        data = [
            {
                "id": e.id,
                "nombre": e.nombre,
                "codigo": e.codigo,
                "pais_id": e.pais_id,
                "fecha_creacion": e.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for e in estados
        ]
        return jsonify(data)
    except Exception as e:
        print(f"[ERROR get_estados]: {e}")
        return jsonify({"error": "No se pudieron obtener los estados/provincias"}), 500


@geolocalizacion_bp.route("/ciudades", methods=["GET"])
def GetCiudad():
    try:
        estado_id = request.args.get("estado_id", type=int)
        if not estado_id:
            return jsonify({"error": "Se requiere el parámetro 'estado_id'"}), 400

        ciudades = CiudadMunicipio.query.filter_by(
            estado_provincia_id=estado_id, activo=True
        ).all()

        data = [
            {
                "id": c.id,
                "nombre": c.nombre,
                "codigo": c.codigo,
                "estado_provincia_id": c.estado_provincia_id,
                "fecha_creacion": c.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for c in ciudades
        ]
        return jsonify(data)
    except Exception as e:
        print(f"[ERROR get_ciudades]: {e}")
        return jsonify({"error": "No se pudieron obtener las ciudades/municipios"}), 500


@geolocalizacion_bp.route("/barrios", methods=["GET"])
def GetBarrio():
    try:
        ciudad_id = request.args.get("ciudad_id", type=int)
        if not ciudad_id:
            return jsonify({"error": "Se requiere el parámetro 'ciudad_id'"}), 400

        barrios = LocalidadBarrio.query.filter_by(
            ciudad_municipio_id=ciudad_id, activo=True
        ).all()

        data = [
            {
                "id": b.id,
                "nombre": b.nombre,
                "codigo_postal": b.codigo_postal,
                "ciudad_municipio_id": b.ciudad_municipio_id,
                "fecha_creacion": b.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for b in barrios
        ]
        return jsonify(data)
    except Exception as e:
        print(f"[ERROR get_barrios]: {e}")
        return jsonify({"error": "No se pudieron obtener los barrios/localidades"}), 500
