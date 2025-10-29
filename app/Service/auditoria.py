from datetime import datetime
import json
import requests
from flask import request
from app.extensions import db
from sqlalchemy import text

def registrarAuditoria(identificacion_consultante, tipo_actividad, descripcion, codigo=None, datos_modificados=None, exito=None):
   

    
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

   
    userAgent = request.headers.get("User-Agent", "Desconocido").lower()
    if "mobile" in userAgent or "android" in userAgent or "iphone" in userAgent:
        dispositivo = "Móvil"
    elif "windows" in userAgent or "macintosh" in userAgent or "linux" in userAgent:
        dispositivo = "PC"
    else:
        dispositivo = "Desconocido"

    
    ubicacion = None
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = resp.json()
        if data.get("status") == "success":
            ciudad = data.get("city", "")
            region = data.get("regionName", "")
            pais = data.get("country", "")
            ubicacion = f"{ciudad}, {region}, {pais}".strip(", ")
        elif ip.startswith("127.") or ip.startswith("192.168.") or ip == "localhost":
            ubicacion = "Red local / desarrollo"
    except Exception as e:
        print(f"No se pudo obtener ubicación: {e}")
        ubicacion = "Desconocida"

    # ✅ Convertir a JSON si datos_modificados es un dict
    if isinstance(datos_modificados, dict):
        datos_modificados = json.dumps(datos_modificados, ensure_ascii=False)

    # Insertar en tabla auditoría
    try:
        sql = text("""
            INSERT INTO auditoria (
                identificacion_consultante, tipo_actividad, descripcion, codigo,
                fecha, ip_origen, dispositivo, ubicacion, datos_modificados, exito
            ) VALUES (
                :identificacion_consultante, :tipo_actividad, :descripcion, :codigo,
                :fecha, :ip_origen, :dispositivo, :ubicacion, :datos_modificados, :exito
            )
        """)
        db.session.execute(sql, {
            "identificacion_consultante": identificacion_consultante,
            "tipo_actividad": tipo_actividad,
            "descripcion": descripcion,
            "codigo": codigo,
            "fecha": datetime.now(),
            "ip_origen": ip,
            "dispositivo": dispositivo,
            "ubicacion": ubicacion,
            "datos_modificados": datos_modificados,
            "exito": exito
        })
        db.session.commit()
    except Exception as e:
        print(f"[ERROR AUDITORIA]: {e}")
        db.session.rollback()
