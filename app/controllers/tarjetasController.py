from flask import Blueprint, request, jsonify, session
from PIL import Image
from app.extensions import db
import pytesseract
import cv2
import numpy as np
import re
from app.models.Tarjetas import Tarjeta
import os
from cryptography.fernet import Fernet


key = os.getenv("FERNET_KEY")
if not key:
    raise RuntimeError("No se encontró la clave de cifrado. Define FERNET_KEY en las variables de entorno")

f = Fernet(key.encode())




card_bp = Blueprint('card', __name__)

def PilToCv(img_pil):
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def OrderPoints(pts):
   
    rect = np.zeros((4,2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def FourPointTransform(image, pts):
    rect = OrderPoints(pts)
    (tl, tr, br, bl) = rect
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxW = max(int(widthA), int(widthB))
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxH = max(int(heightA), int(heightB))
    dst = np.array([[0,0],[maxW-1,0],[maxW-1,maxH-1],[0,maxH-1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, M, (maxW, maxH))

def FindCardContour(image):
    
    h, w = image.shape[:2]
    # reducir tamaño para acelerar
    scale = 600.0 / max(h, w)
    small = cv2.resize(image, (int(w*scale), int(h*scale)))
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edged = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            pts = approx.reshape(4,2) / scale  
            return pts
    return None

def EnhanceForOcr(img):
   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(gray)
    # Denoise
    den = cv2.fastNlMeansDenoising(cl, None, 10, 7, 21)
    # un poco de sharpening
    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    sharp = cv2.filter2D(den, -1, kernel)
    return sharp

def TryMultiscaleOcr(region, config):
    
    results = []
    h, w = region.shape[:2]
    for scale in (1.0, 1.5, 2.0):
        new_w = int(w * scale)
        new_h = int(h * scale)
        scaled = cv2.resize(region, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        text = pytesseract.image_to_string(scaled, config=config)
        results.append(text)
    
    results = [r.strip() for r in results if r.strip()]
    return results[0] if results else ""

def extract_card_number(text):
   
    s = re.sub(r'[^0-9 ]', '', text)
   
    digits = re.sub(r'\s+', '', s)
    m = re.search(r'(\d{13,19})', digits)
    if m:
        num = m.group(1)
       
        return ' '.join([num[i:i+4] for i in range(0, len(num), 4)])
   
    m2 = re.search(r'(\d{4})\D*(\d{4})\D*(\d{4})\D*(\d{4,7})', text)
    if m2:
        num = ''.join(m2.groups())
        return ' '.join([num[i:i+4] for i in range(0, len(num), 4)])
    return None

def ExtractExpiry(text):
   
    m = re.search(r'(0[1-9]|1[0-2])\s*[\/\-]?\s*(\d{2})', text)
    if m:
        return f"{m.group(1)}/{m.group(2)}"
    return None

def ExtractName(text):
    
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    candidates = []
    for l in lines:
        # limpiar caracteres raros
        l_clean = re.sub(r'[^A-ZÑÁÉÍÓÚ ]', '', l.upper())
        if len(l_clean) >= 3 and re.search(r'[A-Z]', l_clean):
            # evitar líneas que sean solo NUMEROS
            if not re.search(r'^\d', l_clean):
                # aceptar si contiene al menos un espacio (nombre y apellido) o varias palabras
                if len(l_clean.split()) >= 2:
                    candidates.append(l_clean)
    if candidates:
        # retorno la más larga (heurística)
        return candidates[0].title()
    # fallback: buscar cualquier palabra larga
    m = re.search(r'([A-Z]{3,}(?: [A-Z]{2,})+)', text)
    if m:
        return m.group(0).title()
    return None



@card_bp.route('/scan_card', methods=['POST'])
def ScanCard():
    if 'card_image' not in request.files:
        return jsonify({"success": False, "error": "No se envió imagen"}), 400

    file = request.files['card_image']
    try:
        image = Image.open(file.stream).convert('RGB')
    except Exception as e:
        return jsonify({"success": False, "error": f"Imagen inválida: {e}"}), 400

    frame = PilToCv(image)  # BGR image

  
    pts = FindCardContour(frame)
    if pts is not None:
        try:
            warp = FourPointTransform(frame, pts)
        except Exception:
            warp = frame.copy()
    else:
        warp = frame.copy()  # fallback: usar imagen original

  
    max_w = 1000
    h, w = warp.shape[:2]
    if w > max_w:
        scale = max_w / w
        warp = cv2.resize(warp, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)

    proc = EnhanceForOcr(warp)

    H, W = proc.shape[:2]
 
    num_region = proc[int(H*0.35):int(H*0.6), int(W*0.05):int(W*0.95)]
    
    expiry_region = proc[int(H*0.58):int(H*0.73), int(W*0.60):int(W*0.95)]
  
    name_region = proc[int(H*0.68):int(H*0.9), int(W*0.05):int(W*0.7)]

   
    config_digits = '-l eng --psm 6 -c tessedit_char_whitelist=0123456789 '
    text_num = TryMultiscaleOcr(num_region, config_digits)
    card_number = extract_card_number(text_num)

   
    if not card_number:
        text_full_digits = TryMultiscaleOcr(proc, config_digits)
        card_number = extract_card_number(text_full_digits)

   
    config_date = '-l eng --psm 6 -c tessedit_char_whitelist=0123456789/ '
    text_exp = TryMultiscaleOcr(expiry_region, config_date)
    expiry = ExtractExpiry(text_exp)
    if not expiry:
        text_full_date = TryMultiscaleOcr(proc, config_date)
        expiry = ExtractExpiry(text_full_date)

   
    config_name = '-l eng --oem 1 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZÑÁÉÍÓÚ '
    text_name = TryMultiscaleOcr(name_region, config_name)
    name = ExtractName(text_name)
    if not name:
        text_full_name = TryMultiscaleOcr(proc, config_name)
        name = ExtractName(text_full_name)

 
    print("OCR num region ->", repr(text_num)[:200])
    print("OCR expiry region ->", repr(text_exp)[:200])
    print("OCR name region ->", repr(text_name)[:200])
    print("EXTRACTED:", card_number, expiry, name)

    success = bool(card_number or expiry or name)
    return jsonify({
        "success": success,
        "cardNumber": card_number or "",
        "cardHolder": name or "",
        "expiryDate": expiry or ""
    })



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