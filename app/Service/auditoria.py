from datetime import datetime
import json
import requests
from flask import request
from app.extensions import db
from sqlalchemy import text
import ipaddress

def registrarAuditoria(identificacion_consultante, tipo_actividad, descripcion, codigo=None, datos_modificados=None, exito=None):
   

    
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip:
       
        ip = ip.split(",")[0].strip()

  
    userAgent = request.headers.get("User-Agent", "desconocido").lower()
    if any(x in userAgent for x in ["mobile", "android", "iphone"]):
        dispositivo = "Móvil"
    elif any(x in userAgent for x in ["windows", "macintosh", "linux"]):
        dispositivo = "PC"
    else:
        dispositivo = "Desconocido"

    
    ubicacion = "Desconocida"
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private:
            ubicacion = "Red interna / desarrollo"
        else:
            # Intentar geolocalizar IP pública
            resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
            data = resp.json()
            if data.get("status") == "success":
                ciudad = data.get("city", "")
                region = data.get("regionName", "")
                pais = data.get("country", "")
                ubicacion = ", ".join(filter(None, [ciudad, region, pais]))
            else:
                ubicacion = "Ubicacion Desconocida"
    except Exception as e:
        print(f"[AUDITORIA] No se pudo obtener ubicación: {e}")

   
    if isinstance(datos_modificados, dict):
        try:
            datos_modificados = json.dumps(datos_modificados, ensure_ascii=False)
        except Exception as e:
            print(f"[AUDITORIA] Error al convertir datos_modificados a JSON: {e}")
            datos_modificados = str(datos_modificados)

    # ─── Insertar en la tabla auditoría ──────────
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
