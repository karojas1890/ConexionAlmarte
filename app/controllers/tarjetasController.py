from flask import Blueprint, request, jsonify, session
from app.extensions import db
from app.models.Tarjetas import Tarjeta
import os
from cryptography.fernet import Fernet
from app.models.APITarjetas import Tarjeta
from app.models.Sinpe import Sinpe
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

key = os.getenv("FERNET_KEY")
if not key:
    raise RuntimeError("No se encontró la clave de cifrado. Define FERNET_KEY en las variables de entorno")

f = Fernet(key.encode())




card_bp = Blueprint('card', __name__)


@card_bp.route('/scan_card', methods=['POST'])
def ScanCard():
    pass


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
@card_bp.route('/delete_card/<int:id_tarjeta>', methods=['DELETE'])
def DeleteCard(id_tarjeta):
    try:
        id_usuario = session.get('idusuario')
        if not id_usuario:
            return jsonify({"success": False, "message": "Usuario no logueado"}), 401

        tarjeta = Tarjeta.query.filter_by(id_tarjeta=id_tarjeta, id_usuario=id_usuario).first()
        if not tarjeta:
            return jsonify({"success": False, "message": "Tarjeta no encontrada"}), 404

        db.session.delete(tarjeta)
        db.session.commit()

        return jsonify({"success": True, "message": "Tarjeta eliminada correctamente"})

    except Exception as e:
        print("Error eliminando tarjeta:", e)
        return jsonify({"success": False, "message": str(e)}), 500

def enmascarar_tarjeta(numero_tarjeta):
    numero_str = str(numero_tarjeta).replace(" ", "").replace("-", "")
    if len(numero_str) <= 4:
        return numero_str
    ultimos_cuatro = numero_str[-4:]
    return "•••• •••• •••• " + ultimos_cuatro

@card_bp.route('/pay', methods=['POST'])
def Pay():
 
    try:
        datos = request.get_json()

        numerotarjeta = datos.get("numerotarjeta")
        nombretarjetahabiente = datos.get("nombretarjetahabiente")
        identificacion = datos.get("identificaciontarjetahabiente")
        codigoseguridad = datos.get("codigoseguridad")
        monto = datos.get("monto")

        # ---------- Validaciones iniciales ----------
        if not numerotarjeta or not codigoseguridad:
            return jsonify({"valido": False, "mensaje": "Número de tarjeta y código de seguridad son obligatorios."}),400

        if not nombretarjetahabiente or nombretarjetahabiente.strip() == "":
            return jsonify({"valido": False, "mensaje": "Nombre del titular es obligatorio."}),400

        if not identificacion or identificacion.strip() == "":
            return jsonify({"valido": False, "mensaje": "Identificacion del titular es obligatoria."}),400

        if not re.fullmatch(r"\d{3}", str(codigoseguridad).strip()):
            return jsonify({"valido": False, "mensaje": "Código de seguridad inválido."}),400

        # ---------- Obtener últimos 4 dígitos ----------
        numero_ingresado = str(numerotarjeta).replace(" ", "").replace("-", "")
        ultimos_cuatro_ingresados = numero_ingresado[-4:]
        print("Buscando tarjeta con últimos 4 dígitos:", ultimos_cuatro_ingresados)

        # ---------- Buscar todas las tarjetas (igual que findAll + find en JS) ----------
        tarjetas = Tarjeta.query.all()

        tarjeta_encontrada = None
        for t in tarjetas:
            # Asegurarse de tratar None y tipos
            numero_db = "" if t.numerotarjeta is None else str(t.numerotarjeta).replace(" ", "").replace("-", "")
            ultimos_cuatro_db = numero_db[-4:]
            if ultimos_cuatro_db == ultimos_cuatro_ingresados:
                tarjeta_encontrada = t
                break

        if not tarjeta_encontrada:
            return jsonify({"valido": False, "mensaje": "Tarjeta no registrada en el sistema."}),404

        tarjeta = tarjeta_encontrada

        # Valida el nombre del titular 
        if (tarjeta.nombretarjetahabiente or "").strip().lower() != (nombretarjetahabiente or "").strip().lower():
            return jsonify({"valido": False, "mensaje": "Nombre del titular incorrecto."}),400

        #  Validaa la identificacion 
        if (tarjeta.identificaciontarjetahabiente or "").strip() != (identificacion or "").strip():
            return jsonify({"valido": False, "mensaje": "Identificacion del titular incorrecta."}),400

        # Validar CVV 
        if (str(tarjeta.codigoseguridad or "")).strip() != str(codigoseguridad).strip():
            return jsonify({"valido": False, "mensaje": "Código de seguridad incorrecto."}),400

        #Validaa estado (0 = activa) 
        try:
            estado_val = int(tarjeta.estado)
        except Exception:
            return ({"valido": False, "mensaje": "Estado de tarjeta inválido."}),400

        if estado_val != 0:
            return jsonify({"valido": False, "mensaje": "Tarjeta inactiva o bloqueada."})

        #  Validaa la fecha de expiracion 
        try:
            mes = int(tarjeta.mesexpira)
            anno = int(tarjeta.annoexpira)
        except Exception:
            return jsonify({"valido": False, "mensaje": "Fecha de expiracion inválida."}),400

        #  expiro
        hoy = datetime.utcnow()
        if (hoy.year, hoy.month) > (anno, mes):
            return jsonify({"valido": False, "mensaje": "La tarjeta ha expirado."}),400

        # Valida el monto si viene 
        monto_num = None
        if monto is not None:
            try:
                # Acepta numeros y strings numericos
                monto_num = Decimal(str(monto))
            except (InvalidOperation, TypeError):
                return jsonify({"valido": False, "mensaje": "Monto inválido."}),400

            if monto_num <= 0:
                return jsonify({"valido": False, "mensaje": "Monto inválido."}),400

            # Compara el saldo
            try:
                saldo_actual = Decimal(str(tarjeta.saldo))
            except Exception:
                # Si no se puede convertir devolver error
                return jsonify({"valido": False, "mensaje": "Saldo de tarjeta no válido."}),400

            if saldo_actual < monto_num:
                return jsonify( {"valido": False, "mensaje": "Saldo insuficiente."}),400

            #Descuenta monto y guarda
            tarjeta.saldo = (saldo_actual - monto_num)
            db.session.add(tarjeta)
            db.session.commit()

        # Respuesta exitosa 
        respuesta = {
            "valido": True,
            "mensaje": "Tarjeta válida."
        }
      
        return  jsonify(respuesta),200

    except Exception as e:
       
        print("Error en validar_tarjeta:", str(e))
        try:
            db.session.rollback()
        except Exception:
            pass
        return jsonify({"valido": False, "mensaje": "Error interno al validar tarjeta.", "error": str(e)}),500

@card_bp.route('/sinpe', methods=['POST'])
def VerificarSinpe():
    datos = request.get_json()

    nreferencia = datos.get("nreferencia")
    ntelefono = datos.get("ntelefono")
    monto = datos.get("monto")

    #validaciones
    if not nreferencia and not ntelefono:
        return jsonify({
            "valido": False,
            "mensaje": "Debe enviar la referencia o el teléfono del SINPE"
        }),400

    if not monto:
        return jsonify({
            "valido": False,
            "mensaje": "Debe enviar el monto del SINPE"
        }),400

    try:
     
        # buscan en la db
        query = Sinpe.query.filter(
            Sinpe.monto == monto,
            Sinpe.estado == 1   
        )

        if nreferencia:
            query = query.filter(Sinpe.nreferencia == nreferencia)

        if ntelefono:
            query = query.filter(Sinpe.ntelefono == ntelefono)

        registro = query.first()

        if not registro:
            return jsonify({
                "valido": False,
                "mensaje": "No se ha encontrado un SINPE válido con los datos proporcionados"
            }),404


        # formatea la  FECHA 
        fechahora_str = registro.fechahora.strftime("%Y-%m-%d %H:%M:%S")

      
        return jsonify({
            "valido": True,
            "mensaje": "SINPE válido, puede agendar la cita",
            "registro": {
                "nreferencia": registro.nreferencia,
                "ntelefono": registro.ntelefono,
                "monto": float(registro.monto),
                "fechahora": fechahora_str,
                "estado": registro.estado
            }
        }),200

    except Exception as e:
        print("Error validando SINPE:", str(e))
        return jsonify({
            "valido": False,
            "mensaje": "Error interno al validar SINPE"
        }), 500