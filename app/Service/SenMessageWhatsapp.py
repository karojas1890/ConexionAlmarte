from twilio.rest import Client
import os
import random
class SMSService:
    def __init__(self):
        self.client = None
        self.sender_number = None

    def init_app(self, app=None):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.sender_number = os.getenv('TWILIO_WHATSAPP_FROM')
        self.client = Client(account_sid, auth_token)


    def BloqueoCuenta(self,userPhone):
    
        mensaje = (
        f"⚠️ Estimado Usuario, su cuenta ha sido bloqueada por múltiples intentos fallidos. "
        "Si fuiste tú, visita: https://conexionalmarte.onrender.com/recuperar_Contra y cambia tu contraseña. "
        "Si no fuiste tú, comunícate con el equipo de soporte."
    )
        print("Número de origen:", self.sender_number)
        print("Número destino:", userPhone)
        try:
            self.client.messages.create(
                from_=self.sender_number,
                to=f"whatsapp:{userPhone}",
                body=mensaje
             )
        
            
            return True  # envío exitoso
        except Exception as e:
           print(f"[Error bloqueo_cuenta] {e}")
           return False  # fallo en el envío


    def SendCodeWhatsapp(self,userPhone, username):
  
        codigo = f"{random.randint(0, 999999):06d}"  

        mensaje = (
         f"🔐 Estimado {username}, tu código de verificación es: *{codigo}*\n\n"
        "Por seguridad, este código es válido por un tiempo limitado.\n\n"
        "Si no solicitaste este código, ignora este mensaje."
       )

        try:
           self.client.messages.create(
            from_=self.sender_number,
            to=f"whatsapp:{userPhone}",
            body=mensaje
           )
           return codigo 
        except Exception as e:
           print(f"[Error send_code] {e}")
           return None
