import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
#SOLO EN LOCALHOST
#from dotenv import load_dotenv

#Sload_dotenv()

import threading
class EmailService:
    def __init__(self):
    
        self.sender_email = None
        self.api_key = None

    def init_app(self, app):
       
        self.sender_email = os.getenv('FROM_EMAIL')
        self.api_key = os.getenv('SENDGRID_API_KEY')

       

    def send_email(self, to_email, subject, html_body):
        try:
            message = Mail(
                from_email=self.sender_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_body
            )
            
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
           
            return True
            
        except Exception as e:
            print(f" Error enviando correo: {e}")
            return False

            
        except Exception as e:
            print(f"[ERROR] Error enviando correo: {e}")
    #  template para cita
    def SendNewAppointment(self, mail, pacient, date, nombreServicio):
        try:
            subject = "Tienes una nueva cita - Conexión Almarte"
            html = f"""
                <!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Nueva Cita Agendada</title>
                </head>
                <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
                    <table role="presentation" style="max-width: 600px; width: 100%; margin: 0 auto; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 30px 15px;">
                                 <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            <!-- Header con gradiente -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); padding: 40px 30px; text-align: center;">
                                    <div style="width: 60px; height: 60px; background: white; border-radius: 12px; margin: 0 auto 20px; display: inline-block; line-height: 60px; font-size: 28px; font-weight: bold; color: #5BA8A0;">
                                        AM
                                    </div>
                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600;">
                                        🔔 Nueva Cita Agendada
                                    </h1>
                                    <p style="margin: 10px 0 0; color: #ffffff; font-size: 16px; opacity: 0.95;">
                                        Un paciente ha reservado una sesión contigo
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Contenido principal -->
                            <tr>
                                <td style="padding: 40px 30px;">
                                    <p style="margin: 0 0 30px; color: #333333; font-size: 16px; line-height: 1.6; text-align: center;">
                                        Se ha agendado una nueva cita en tu agenda profesional
                                    </p>
                                    
                                    <!-- Tarjeta de información de la cita -->
                                    <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 30px;">
                                        <tr>
                                            <td style="background: linear-gradient(135deg, #f8fafa 0%, #e8f5f4 100%); border-radius: 12px; padding: 25px; border: 2px solid #5BA8A0;">
                                                <p style="margin: 0 0 20px; color: #5BA8A0; font-size: 18px; font-weight: 600; text-align: center; text-transform: uppercase; letter-spacing: 1px;">
                                                    Detalles de la Cita
                                                </p>
                                                
                                                <!-- Paciente -->
                                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 15px;">
                                                    <tr>
                                                        <td style="padding: 12px; background-color: #ffffff; border-radius: 8px;">
                                                            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                                <tr>
                                                                    <td style="width: 40px; vertical-align: top;">
                                                                        <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; line-height: 32px; text-align: center;">
                                                                            👤
                                                                        </div>
                                                                    </td>
                                                                    <td style="padding-left: 12px;">
                                                                        <p style="margin: 0; color: #666666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Paciente</p>
                                                                        <p style="margin: 5px 0 0; color: #333333; font-size: 16px; font-weight: 600;">{pacient}</p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Fecha y Hora -->
                                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 15px;">
                                                    <tr>
                                                        <td style="padding: 12px; background-color: #ffffff; border-radius: 8px;">
                                                            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                                <tr>
                                                                    <td style="width: 40px; vertical-align: top;">
                                                                        <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; line-height: 32px; text-align: center;">
                                                                            📅
                                                                        </div>
                                                                    </td>
                                                                    <td style="padding-left: 12px;">
                                                                        <p style="margin: 0; color: #666666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Fecha y Hora</p>
                                                                        <p style="margin: 5px 0 0; color: #333333; font-size: 16px; font-weight: 600;">{date}</p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Servicio -->
                                                <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                    <tr>
                                                        <td style="padding: 12px; background-color: #ffffff; border-radius: 8px;">
                                                            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                                <tr>
                                                                    <td style="width: 40px; vertical-align: top;">
                                                                        <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; line-height: 32px; text-align: center;">
                                                                            📋
                                                                        </div>
                                                                    </td>
                                                                    <td style="padding-left: 12px;">
                                                                        <p style="margin: 0; color: #666666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Tipo de Servicio</p>
                                                                        <p style="margin: 5px 0 0; color: #333333; font-size: 16px; font-weight: 600;">{nombreServicio}</p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Acciones rápidas -->
                                    <div style="background-color: #e8f5f4; border-left: 4px solid #5BA8A0; padding: 15px; border-radius: 8px; margin: 0 0 25px;">
                                        <p style="margin: 0 0 10px; color: #4A9B94; font-size: 14px; font-weight: 600;">
                                            📌 Acciones recomendadas:
                                        </p>
                                        <ul style="margin: 0; padding-left: 20px; color: #4A9B94; font-size: 14px; line-height: 1.6;">
                                            <li>Revisa el historial del paciente antes de la sesión</li>
                                            <li>Prepara los materiales necesarios para el servicio</li>
                                            <li>Confirma que tienes disponibilidad en ese horario</li>
                                        </ul>
                                    </div>
                                    
                                    <!-- Botón de acción -->
                                    <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 20px;">
                                        <tr>
                                            <td style="text-align: center;">
                                                <a href="[URL_DE_TU_APP]/therapist-appointments" style="display: inline-block; background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); color: #ffffff; text-decoration: none; padding: 14px 40px; border-radius: 8px; font-size: 16px; font-weight: 600; box-shadow: 0 2px 4px rgba(91, 168, 160, 0.3);">
                                                    Ver Mi Agenda
                                                </a>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <p style="margin: 0; color: #666666; font-size: 14px; line-height: 1.6; text-align: center;">
                                        Esta cita se ha agregado automáticamente a tu agenda.
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f8fafa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                                    <p style="margin: 0 0 10px; color: #5BA8A0; font-size: 18px; font-weight: 600;">
                                        Conexión by Almarte
                                    </p>
                                    <p style="margin: 0 0 15px; color: #666666; font-size: 14px;">
                                        Plataforma Profesional para Terapeutas
                                    </p>
                                    <p style="margin: 0; color: #999999; font-size: 12px; line-height: 1.6;">
                                        Este es un correo automático, por favor no respondas a este mensaje.<br>
                                        Si necesitas ayuda, contáctanos a través de la plataforma.
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
            thread = threading.Thread(target=self.send_email, args=(mail, subject, html))
            thread.start()
        
        except Exception as e:
          print (e)
          
    def SendNewAppointmentPacient(self, mail, pacient, date, nombreServicio,nombreTerapeuta):
      try:
        subject = "Confirmación de tu cita - Conexión by Almarte"
        html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirmación de Cita</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="max-width: 600px; width: 100%; margin: 0 auto; border-collapse: collapse;">
            <tr>
                <td style="padding: 30px 15px;">
                    <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <!-- Header con gradiente -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); padding: 40px 30px; text-align: center;">
                                <div style="width: 60px; height: 60px; background: white; border-radius: 12px; margin: 0 auto 20px; display: inline-block; line-height: 60px; font-size: 28px; font-weight: bold; color: #5BA8A0;">
                                    AM
                                </div>
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600;">
                                    ✓ Cita Confirmada
                                </h1>
                                <p style="margin: 10px 0 0; color: #ffffff; font-size: 16px; opacity: 0.95;">
                                    Tu sesión ha sido agendada exitosamente
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Contenido principal -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <p style="margin: 0 0 30px; color: #333333; font-size: 16px; line-height: 1.6; text-align: center;">
                                    Hola <strong style="color: #5BA8A0;">{pacient}</strong>, gracias por confiar en los servicios de <strong>AlmarteCR</strong>
                                </p>
                                
                                <!-- Tarjeta de información de la cita -->
                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 30px;">
                                    <tr>
                                        <td style="background: linear-gradient(135deg, #f8fafa 0%, #e8f5f4 100%); border-radius: 12px; padding: 25px; border: 2px solid #5BA8A0;">
                                            <p style="margin: 0 0 20px; color: #5BA8A0; font-size: 18px; font-weight: 600; text-align: center; text-transform: uppercase; letter-spacing: 1px;">
                                                Detalles de tu Cita
                                            </p>
                                            
                                            <!-- Servicio -->
                                            <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 15px;">
                                                <tr>
                                                    <td style="padding: 12px; background-color: #ffffff; border-radius: 8px;">
                                                        <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                            <tr>
                                                                <td style="width: 40px; vertical-align: top;">
                                                                    <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; line-height: 32px; text-align: center;">
                                                                        📋
                                                                    </div>
                                                                </td>
                                                                <td style="padding-left: 12px;">
                                                                    <p style="margin: 0; color: #666666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Servicio</p>
                                                                    <p style="margin: 5px 0 0; color: #333333; font-size: 16px; font-weight: 600;">{nombreServicio}</p>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            
                                            <!-- Fecha y Hora -->
                                            <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 15px;">
                                                <tr>
                                                    <td style="padding: 12px; background-color: #ffffff; border-radius: 8px;">
                                                        <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                            <tr>
                                                                <td style="width: 40px; vertical-align: top;">
                                                                    <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; line-height: 32px; text-align: center;">
                                                                        📅
                                                                    </div>
                                                                </td>
                                                                <td style="padding-left: 12px;">
                                                                    <p style="margin: 0; color: #666666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Fecha y Hora</p>
                                                                    <p style="margin: 5px 0 0; color: #333333; font-size: 16px; font-weight: 600;">{date}</p>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            
                                            <!-- Terapeuta -->
                                            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                <tr>
                                                    <td style="padding: 12px; background-color: #ffffff; border-radius: 8px;">
                                                        <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                            <tr>
                                                                <td style="width: 40px; vertical-align: top;">
                                                                    <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; line-height: 32px; text-align: center;">
                                                                        👩‍⚕️
                                                                    </div>
                                                                </td>
                                                                <td style="padding-left: 12px;">
                                                                    <p style="margin: 0; color: #666666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Profesional</p>
                                                                    <p style="margin: 5px 0 0; color: #333333; font-size: 16px; font-weight: 600;">Licda. {nombreTerapeuta}</p>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Recordatorio -->
                                <div style="background-color: #e8f5f4; border-left: 4px solid #5BA8A0; padding: 15px; border-radius: 8px; margin: 0 0 25px;">
                                    <p style="margin: 0 0 10px; color: #4A9B94; font-size: 14px; font-weight: 600;">
                                        💡 Recordatorio importante:
                                    </p>
                                    <ul style="margin: 0; padding-left: 20px; color: #4A9B94; font-size: 14px; line-height: 1.6;">
                                        <li>Te recomendamos llegar 5 minutos antes de tu cita</li>
                                        <li>Si necesitas cancelar o reprogramar, hazlo con al menos 24 horas de anticipación</li>
                                        <li>Prepara cualquier pregunta o tema que desees abordar en la sesión</li>
                                    </ul>
                                </div>
                                
                                
                                
                                <p style="margin: 0; color: #666666; font-size: 14px; line-height: 1.6; text-align: center;">
                                    Si tienes alguna pregunta, no dudes en contactarnos.
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
        thread = threading.Thread(target=self.send_email, args=(mail, subject, html))
        thread.start()
        
      except Exception as e:
          print (e)
          
    #para nuevo usuario
    def SendNewUser(self, email, username, password):
      try: 
        subject = "Bienvenido a Conexión by Almarte - Tus credenciales de acceso"
        html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bienvenido a Almarte</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="max-width: 600px; width: 100%; margin: 0 auto; border-collapse: collapse;">
            <tr>
                <td style="padding: 30px 15px;">
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
                                
                               
            
                                <!-- Botón de acción -->
                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 0 0 25px;">
                                    <tr>
                                        <td style="text-align: center;">
                                            <a href="https://conexionalmarte.onrender.com" style="display: inline-block; background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); color: #ffffff; text-decoration: none; padding: 14px 40px; border-radius: 8px; font-size: 16px; font-weight: 600; box-shadow: 0 2px 4px rgba(91, 168, 160, 0.3);">
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
        thread = threading.Thread(target=self.send_email, args=(email, subject, html))
        thread.start()
      except Exception as e:
          print (e)
   
       
       
    def SendUsernameReminder(self, email, uss):
        try:
            subject = "Recuperación de usuario - Conexión by Almarte"
            html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Recuperación de usuario</title>
            </head>
            <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
                <table role="presentation" style="max-width: 600px; width: 100%; margin: 0 auto; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 30px 15px;">
                            <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        
                        <tr>
                            <td style="background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%); padding: 40px 30px; text-align: center;">
                                <div style="width: 60px; height: 60px; background: white; border-radius: 12px; margin: 0 auto 20px; display: inline-block; line-height: 60px; font-size: 28px; font-weight: bold; color: #5BA8A0;">
                                    AM
                                </div>
                                <h1 style="margin: 0; color: #ffffff; font-size: 26px; font-weight: 600;">
                                    Recuperación de usuario
                                </h1>
                                <p style="margin: 10px 0 0; color: #ffffff; font-size: 16px;">
                                    Hola, hemos encontrado tu nombre de usuario registrado en Conexión by Almarte.
                                </p>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 40px 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    A continuación encontrarás tu usuario de acceso:
                                </p>

                                <div style="background-color: #f8fafa; border-left: 4px solid #5BA8A0; padding: 20px; border-radius: 8px; margin: 20px 0;">
                                    <p style="margin: 0; font-size: 18px; font-weight: 600; color: #333333;">👤 Usuario: {uss}</p>
                                </div>

                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 25px 0;">
                                    <tr>
                                        <td style="text-align: center;">
                                            <a href="https://conexionalmarte.onrender.com" 
                                               style="display: inline-block; background: linear-gradient(135deg, #5BA8A0 0%, #4A9B94 100%);
                                                      color: #ffffff; text-decoration: none; padding: 14px 40px;
                                                      border-radius: 8px; font-size: 16px; font-weight: 600;">
                                                Iniciar sesión
                                            </a>
                                        </td>
                                    </tr>
                                </table>

                                <p style="color: #666666; font-size: 14px;">
                                    Si no solicitaste esta información, puedes ignorar este correo de forma segura.
                                </p>
                            </td>
                        </tr>

                        <tr>
                            <td style="background-color: #f8fafa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                                <p style="margin: 0 0 10px; color: #5BA8A0; font-size: 18px; font-weight: 600;">
                                    Conexión Almarte
                                </p>
                                <p style="margin: 0 0 15px; color: #666666; font-size: 14px;">
                                    Tu bienestar mental es nuestra prioridad
                                </p>
                                <p style="margin: 0; color: #999999; font-size: 12px;">
                                    Este es un mensaje automático, por favor no respondas a este correo.
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
        except Exception as e:
          print (e)
    
    def SendVerificationCode(self, email, username, code):
        try:
            subject = "Tu código de verificación - Conexión by Almarte"
            html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Código de Verificación</title>
            </head>
            <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
                <table role="presentation" style="max-width: 600px; width: 100%; margin: 0 auto; border-collapse: collapse;">
                  <tr>
                       <td style="padding: 30px 15px;">
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
        except Exception as e:
          print (e)
        
    def SendVerificationCodeCredentials(self, email, username, code):
        try: 
            subject = "Tu código de verificación - Conexión by Almarte"
            html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Código de Verificación</title>
            </head>
            <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
                <table role="presentation" style="max-width: 600px; width: 100%; margin: 0 auto; border-collapse: collapse;">
                     <tr>
                        <td style="padding: 30px 15px;">
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
                                    Hemos recibido una solicitud para restablecer su cuenta. Utiliza el siguiente código para completar el proceso:
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
        except Exception as e:
          print (e)