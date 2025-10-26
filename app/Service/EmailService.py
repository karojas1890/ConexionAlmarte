import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app
import threading
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
          with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
            server.starttls()
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
          
    def SendNewAppointmentPacient(self, mail, pacient, date, nombreServicio,nombreTerapeuta):
      try:
        subject = "Confirmación de cita. - Conexion"
        html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 10px; padding: 30px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            
            <img 
                 alt="Logo Conexion" 
                 style="max-width: 150px; margin-bottom: 20px;" />
            
            <h2 style="color: #333; margin-bottom: 10px;">Gracias por confiar en los servicios de AlmarteCR</h2>
            <p style="font-size: 16px; color: #555; margin-bottom: 5px;">Hola: <b>{pacient}</b></p>
            <p style="font-size: 16px; color: #555; margin-bottom: 5px;">Su cita en: <b>{nombreServicio}</b></p>
            <p style="font-size: 16px; color: #555; margin-bottom: 20px;">Es el: <b>{date}</b></p>
            <p style="font-size: 16px; color: #555; margin-bottom: 20px;">Con la Licda: <b>{nombreTerapeuta}</b></p>
            
            
              
        </div>
    </div>
    """
        self.send_email(mail, subject, html)
        
      except Exception as e:
          print (e)
          
    #para nuevo usuario
    def SendNewUser(self, email, username, password):
        subject = "Bienvenido a Conexión by Almarte - Tus Credenciales de Acceso"
        html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bienvenido a Almarte</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                       
                        <tr>
                            <td style="background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); padding: 40px 30px; text-align: center;">
                                <div style="width: 60px; height: 60px; background: white; border-radius: 12px; margin: 0 auto 20px; display: inline-block; line-height: 60px; font-size: 28px; font-weight: bold; color: #5BA8A0;">
                                    AM
                                </div>
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600;">
                                    ¡Bienvenido a Conexión by Almarte!
                                </h1>
                                <p style="margin: 10px 0 0; color: #ffffff; font-size: 16px; opacity: 0.95;">
                                    Tu espacio de bienestar mental
                                </p>
                            </td>
                        </tr>
                        
                     
                        <tr>
                            <td style="padding: 40px 30px;">
                                <p style="margin: 0 0 20px; color: #333333; font-size: 16px; line-height: 1.6;">
                                    Nos alegra que formes parte de la familia Almarte. Tu cuenta ha sido creada exitosamente y ya puedes comenzar tu camino hacia el bienestar.
                                </p>
                                
                                <p style="margin: 0 0 25px; color: #333333; font-size: 16px; line-height: 1.6;">
                                    A continuación encontrarás tus credenciales de acceso:
                                </p>
                                
                                <!-- Credenciales -->
                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 30px;">
                                    <tr>
                                        <td style="background-color: #f8fafa; border-left: 4px solid #5BA8A0; padding: 20px; border-radius: 8px;">
                                            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                <tr>
                                                    <td style="padding: 8px 0;">
                                                        <span style="color: #666666; font-size: 14px; display: block; margin-bottom: 5px;">Usuario:</span>
                                                        <span style="color: #333333; font-size: 18px; font-weight: 600; display: block;">{username}</span>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 8px 0; border-top: 1px solid #e0e0e0;">
                                                        <span style="color: #666666; font-size: 14px; display: block; margin-bottom: 5px;">Contraseña:</span>
                                                        <span style="color: #333333; font-size: 18px; font-weight: 600; display: block; font-family: 'Courier New', monospace;">{password}</span>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                                
                               
                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 25px;">
                                    <tr>
                                        <td style="text-align: center;">
                                            <a href="" style="display: inline-block; background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); color: #ffffff; text-decoration: none; padding: 14px 40px; border-radius: 8px; font-size: 16px; font-weight: 600; box-shadow: 0 2px 4px rgba(91, 168, 160, 0.3);">
                                                Iniciar Sesión
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Recomendaciones de seguridad -->
                                <div style="background-color: #fff8e6; border-left: 4px solid #ffc107; padding: 15px; border-radius: 8px; margin: 0 0 20px;">
                                    <p style="margin: 0 0 10px; color: #856404; font-size: 14px; font-weight: 600;">
                                        🔒 Recomendaciones de seguridad:
                                    </p>
                                    <ul style="margin: 0; padding-left: 20px; color: #856404; font-size: 14px; line-height: 1.6;">
                                        <li>Te recomendamos cambiar tu contraseña antes del primer inicio de sesión</li>
                                        <li>No compartas tus credenciales con nadie</li>
                                        <li>Mantén tu información de acceso segura</li>
                                    </ul>
                                </div>
                                
                                <p style="margin: 0; color: #666666; font-size: 14px; line-height: 1.6;">
                                    Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f8fafa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                                <p style="margin: 0 0 10px; color: #5BA8A0; font-size: 18px; font-weight: 600;">
                                    Conexión Almarte
                                </p>
                                <p style="margin: 0 0 15px; color: #666666; font-size: 14px;">
                                    Tu bienestar mental es nuestra prioridad
                                </p>
                                <p style="margin: 0; color: #999999; font-size: 12px; line-height: 1.6;">
                                    Este es un correo automático, por favor no respondas a este mensaje.<br>
                                    Si necesitas ayuda, contáctanos a través de nuestra plataforma.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
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
        
    def SendVerificationCode(self, email, username, code):
        subject = "Código de Verificación - Conexión by Almarte"
        html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Código de Verificación</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                      
                        <tr>
                            <td style="background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); padding: 40px 30px; text-align: center;">
                                <div style="width: 60px; height: 60px; background: white; border-radius: 12px; margin: 0 auto 20px; display: inline-block; line-height: 60px; font-size: 28px; font-weight: bold; color: #5BA8A0;">
                                    AM
                                </div>
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600;">
                                    Código de Verificación
                                </h1>
                                <p style="margin: 10px 0 0; color: #ffffff; font-size: 16px; opacity: 0.95;">
                                    Verifica tu identidad
                                </p>
                            </td>
                        </tr>
                        
                      
                        <tr>
                            <td style="padding: 40px 30px;">
                                <p style="margin: 0 0 20px; color: #333333; font-size: 16px; line-height: 1.6;">
                                    Hola <strong>{username}</strong>,
                                </p>
                                
                                <p style="margin: 0 0 30px; color: #333333; font-size: 16px; line-height: 1.6;">
                                    Hemos recibido una solicitud para verificar tu cuenta. Utiliza el siguiente código para completar el proceso:
                                </p>
                                
                              
                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 30px;">
                                    <tr>
                                        <td style="text-align: center; padding: 30px; background: linear-gradient(135deg, #f8fafa 0%, #e8f5f4 100%); border-radius: 12px; border: 2px dashed #5BA8A0;">
                                            <p style="margin: 0 0 15px; color: #666666; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
                                                Tu Código de Verificación
                                            </p>
                                            <p style="margin: 0; color: #5BA8A0; font-size: 42px; font-weight: 700; letter-spacing: 8px; font-family: 'Courier New', monospace;">
                                                {code}
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                                
                                
                                <div style="background-color: #fff8e6; border-left: 4px solid #ffc107; padding: 15px; border-radius: 8px; margin: 0 0 25px;">
                                    <p style="margin: 0 0 10px; color: #856404; font-size: 14px; font-weight: 600;">
                                        ⏱️ Información importante:
                                    </p>
                                    <ul style="margin: 0; padding-left: 20px; color: #856404; font-size: 14px; line-height: 1.6;">
                                        <li>Este código es válido por <strong>10 minutos</strong></li>
                                        <li>Solo puede ser utilizado una vez</li>
                                        <li>No compartas este código con nadie</li>
                                    </ul>
                                </div>
                                
                                
                                <div style="background-color: #ffebee; border-left: 4px solid #f44336; padding: 15px; border-radius: 8px; margin: 0 0 20px;">
                                    <p style="margin: 0; color: #c62828; font-size: 14px; line-height: 1.6;">
                                        <strong>🔒 ¿No solicitaste este código?</strong><br>
                                        Si no reconoces esta actividad, ignora este correo y considera cambiar tu contraseña de inmediato.
                                    </p>
                                </div>
                                
                                <p style="margin: 0; color: #666666; font-size: 14px; line-height: 1.6; text-align: center;">
                                    Si tienes problemas, contáctanos a través de nuestra plataforma.
                                </p>
                            </td>
                        </tr>
                        
                    
                        <tr>
                            <td style="background-color: #f8fafa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                                <p style="margin: 0 0 10px; color: #5BA8A0; font-size: 18px; font-weight: 600;">
                                    Conexión by Almarte
                                </p>
                                <p style="margin: 0 0 15px; color: #666666; font-size: 14px;">
                                    Tu bienestar mental es nuestra prioridad
                                </p>
                                <p style="margin: 0; color: #999999; font-size: 12px; line-height: 1.6;">
                                    Este es un correo automático, por favor no respondas a este mensaje.<br>
                                    Si necesitas ayuda, contáctanos a través de nuestra plataforma.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
        thread = threading.Thread(target=self.send_email, args=(email, subject, html))
        thread.start()
        