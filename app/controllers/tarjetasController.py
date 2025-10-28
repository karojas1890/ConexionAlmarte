from flask import Blueprint, request, jsonify, session
from app.extensions import db

from app.models.Tarjetas import Tarjeta
import os
from cryptography.fernet import Fernet


key = os.getenv("FERNET_KEY")
if not key:
    raise RuntimeError("No se encontró la clave de cifrado. Define FERNET_KEY en las variables de entorno")

f = Fernet(key.encode())




card_bp = Blueprint('card', __name__)



@card_bp.route('/add_card', methods=['POST'])
def AddCard():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No se recibieron datos"}), 400

        fechaExpiracion = data.get('expiryDate')
        numeroTarjeta = data.get('cardNumber')
        ultimos4 = numeroTarjeta[-4:]
        idusuario = session.get('idusuario')

        print(idusuario)
        numeroCifrado = f.encrypt(numeroTarjeta.encode()).decode('utf-8')
        fechaCifrada = f.encrypt(fechaExpiracion.encode()).decode('utf-8')

        nueva_tarjeta = Tarjeta(
            id_usuario=idusuario,
            nombre_titular=data.get('cardHolder'),
            ultimo4=ultimos4,
            numero_tarjeta=numeroCifrado,
            fecha_expiracion=fechaCifrada,
            estado=True
        )

        db.session.add(nueva_tarjeta)
        db.session.commit()

        return jsonify({"success": True, "message": "Tarjeta agregada correctamente"})

    except Exception as e:
        print("Error agregando tarjeta:", e)
        return jsonify({"success": False, "message": str(e)}), 500
    
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from flask import session, jsonify

load_dotenv()  # sólo necesario si usas .env en desarrollo

key = os.getenv("FERNET_KEY")
if not key:
    raise RuntimeError("No se encontró la clave de cifrado. Define FERNET_KEY en .env o en las variables de entorno")

f = Fernet(key.encode())

@card_bp.route('/get_cards', methods=['GET'])
def GetCards():
    try:
        id_usuario = session.get('idusuario')
        if not id_usuario:
            return jsonify({"success": False, "message": "Usuario no logueado"}), 401

        tarjetas = Tarjeta.query.filter_by(id_usuario=id_usuario).all()

        tarjetas_data = []
        for t in tarjetas:
            
            fecha = None
            try:
                if t.fecha_expiracion:
                   
                    fecha = f.decrypt(t.fecha_expiracion.encode()).decode()
            except Exception as err:
                
                print(f"Warning: no se pudo descifrar fecha para tarjeta {t.id_tarjeta}: {err}")
                fecha = None

            tarjetas_data.append({
                "id_tarjeta": t.id_tarjeta,
                "nombre_titular": t.nombre_titular,
                "ultimo4": t.ultimo4,
                "fecha_expiracion": fecha 
            })

        return jsonify(tarjetas_data)

    except Exception as e:
        print("Error obteniendo tarjetas:", e)
        return jsonify({"success": False, "message": str(e)}), 500
