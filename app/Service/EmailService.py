import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app

class emailService:
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        self.smtp_server = app.config['EMAIL_SETTINGS']['SMTP_SERVER']
        self.smtp_port = app.config['EMAIL_SETTINGS']['SMTP_PORT']
        self.sender_email = app.config['EMAIL_SETTINGS']['SENDER_EMAIL']
        self.sender_password = app.config['EMAIL_SETTINGS']['SENDER_PASSWORD']

    def send_email(self, to_email, subject, html_body):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)

    #  template para cita
    def SendNewAppointment(self, mail, pacient, date):
        subject = "Nueva cita agendada - Conexion"
        html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 10px; padding: 30px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            
            <img  
                 alt="Logo JOKAVE" 
                 style="max-width: 150px; margin-bottom: 20px;" />
            
            <h2 style="color: #333; margin-bottom: 10px;">¡Nueva cita agendada!</h2>
            <p style="font-size: 16px; color: #555; margin-bottom: 5px;">Paciente: <b>{pacient}</b></p>
            <p style="font-size: 16px; color: #555; margin-bottom: 20px;">Fecha/Hora: <b>{date}</b></p>
            
            
            <a href="#" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Ver Citas</a>
            
        </div>
    </div>
    """
        self.send_email(mail, subject, html)


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
