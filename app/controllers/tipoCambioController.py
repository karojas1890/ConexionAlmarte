from flask import Flask, jsonify, Blueprint
import requests
import datetime
import re
import os
#from dotenv import load_dotenv

#load_dotenv()

tipoCambio_bp = Blueprint('tpc', __name__)

BCCR_TOKEN = os.getenv("BCCR_TOKEN")
BCCR_NAME = os.getenv("BCCR_NAME")
BCCR_EMAIL = os.getenv("BCCR_EMAIL")  # <- agregar el correo en .env
def ExtraerTipoCambio(xml_string, indicador):
    try:
        
        
        valores = re.findall(r'<NUM_VALOR>([^<]+)</NUM_VALOR>', xml_string)
        
        
        if valores:
            valor = float(valores[0])
            
            return valor
        else:
           
            return None
    except Exception as e:
        
        return None

@tipoCambio_bp.route('/tipo_cambio', methods=['GET'])
def ConsultarTipoCambio():
    url = "https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/ObtenerIndicadoresEconomicos"
    fecha = datetime.datetime.now().strftime("%d/%m/%Y")  

   

    try:
        # Consultar indicador 317 (Compra)
        data_compra = {
            'Indicador': '317',  
            'FechaInicio': fecha,
            'FechaFinal': fecha,
            'Nombre': BCCR_NAME,
            'SubNiveles': 'N',
            'CorreoElectronico': BCCR_EMAIL,  
            'Token': BCCR_TOKEN
        }

        # Consultar indicador 318 (Venta)
        data_venta = {
            'Indicador': '318',  
            'FechaInicio': fecha,
            'FechaFinal': fecha,
            'Nombre': BCCR_NAME,
            'SubNiveles': 'N',
            'CorreoElectronico': BCCR_EMAIL,  
            'Token': BCCR_TOKEN
        }

        headers = {
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Accept": "application/xml"
        }

        # Realizar ambas consultas
        
        response_compra = requests.post(url, data=data_compra, headers=headers, timeout=30)
        response_compra.raise_for_status()
        compra = ExtraerTipoCambio(response_compra.text, '317')

        
        response_venta = requests.post(url, data=data_venta, headers=headers, timeout=30)
        response_venta.raise_for_status()
        venta = ExtraerTipoCambio(response_venta.text, '318')

     

        # Validar que se obtuvieron ambos valores
        if compra is not None and venta is not None:
            resultado = {
                "compra": float(compra),
                "venta": float(venta),
                "fecha_consulta": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
           
            return jsonify(resultado)
        else:
            error_msg = {
                "error": "No se pudieron obtener ambos valores del tipo de cambio",
                "compra_obtenido": compra is not None,
                "venta_obtenido": venta is not None,
                "compra_valor": compra,
                "venta_valor": venta
            }
            
            return jsonify(error_msg), 500

    except requests.RequestException as e:
        error_msg = {"error": "Error al consultar el API externo", "detalle": str(e)}
        
        return jsonify(error_msg), 500