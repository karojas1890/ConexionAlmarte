import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app

class EmailService:
    def __init__(self):
    
        self.smtp_server = None
        self.smtp_port = None
        self.sender_email = None
        self.sender_password = None

    def init_app(self, app):
       
        settings = app.config.get("EMAIL_SETTINGS")
        

        self.smtp_server = settings.get("SMTP_SERVER")
        self.smtp_port = settings.get("SMTP_PORT")
        self.sender_email = settings.get("SENDER_EMAIL")
        self.sender_password = settings.get("SENDER_PASSWORD")

        

    def send_email(self, to_email, subject, html_body):
        try:
            
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(html_body, "html"))
        except Exception as ex:
            print(ex)
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()           
                server.starttls()        
                server.ehlo()           
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
        except Exception as e:
            print(f"[ERROR] Error enviando correo: {e}")
    #  template para cita
    def SendNewAppointment(self, mail, pacient, date, nombreServicio):
      try:
        subject = "Nueva cita agendada - Conexion"
        html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 10px; padding: 30px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            
            <img 
                 alt="Logo Conexion" 
                 style="max-width: 150px; margin-bottom: 20px;" />
            
            <h2 style="color: #333; margin-bottom: 10px;">¡Nueva cita agendada!</h2>
            <p style="font-size: 16px; color: #555; margin-bottom: 5px;">Paciente: <b>{pacient}</b></p>
            <p style="font-size: 16px; color: #555; margin-bottom: 20px;">Fecha/Hora: <b>{date}</b></p>
            <p style="font-size: 16px; color: #555; margin-bottom: 5px;">Tipo de Servicio: <b>{nombreServicio}</b></p>
            
              
        </div>
    </div>
    """
        self.send_email(mail, subject, html)
        
      except Exception as e:
          print (e)
          

    # Template para nuevo usuario
    def send_new_user(self, email, username, password):
        subject = "Datos de acceso"
        html = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Bienvenido</h2>
            <p>Usuario: <b>{username}</b></p>
            <p>Contraseña: <b>{password}</b></p>
        </div>
        """
        self.send_email(email, subject, html)

    # Template para tutor
    def send_tutor_info(self, tutor_email, minor_name, username, pin):
        subject = "Datos de acceso del menor"
        html = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Acceso al perfil del menor</h2>
            <p>Nombre del menor: <b>{minor_name}</b></p>
            <p>Usuario: <b>{username}</b></p>
            <p>PIN: <b>{pin}</b></p>
        </div>
        """
        self.send_email(tutor_email, subject, html)
