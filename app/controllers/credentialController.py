
from flask import Blueprint, request, jsonify,session,url_for
from app.extensions import db
from app.models.consultante import Consultante
from app.models.user import Usuario
from app.models.Terapeuta import Terapeuta
from app.Service import email_service
import random
import bcrypt
from app.Service.auditoria import registrarAuditoria
from datetime import datetime
from app.models.passRestriccion import RestriccionPassword
import unicodedata
credential_bp = Blueprint("crede", __name__)


@credential_bp.route('/validar_usuario', methods=['POST'])
def ValidarUsuarioRecovery():
    try:
        data = request.get_json()
        usuario_input = data.get('usuario')
        tipo_recuperacion = data.get('tipo')
        session['recovery_tipo'] = tipo_recuperacion
        if not usuario_input:
            return jsonify({'success': False, 'message': 'Correo requerido'})

       
        consultante = Consultante.query\
            .filter(Consultante.correo == usuario_input)\
            .first()

        if consultante:
           
            usuario = Usuario.query.filter(Usuario.idusuario == consultante.idusuario).first()
            if not usuario:
                return jsonify({'success': False, 'message': 'Error: Usuario no encontrado'})

            if usuario.estado != 1 and tipo_recuperacion!="1":
                session['recovery_estado'] = usuario.estado
                return jsonify({
                    'success': False,
                    'message': 'Usuario bloqueado. Para reactivar tu cuenta, por favor utiliza la opción de "Recuperar Contraseña" para restablecer tus credenciales.'
                })

          
            session['recovery_tipo_usuario'] = 'consultante'  
            session['recovery_idusuario'] = usuario.idusuario
            session['recovery_identificacion'] = consultante.identificacion
            session['recovery_tipo'] = tipo_recuperacion
            session['recovery_correo'] = consultante.correo  
            session['recovery_nombre'] = consultante.nombre
            session['recovery_estado'] = usuario.estado
            session['recovery_usuario'] = usuario.usuario
            session['recovery_date']=consultante.fechanacimiento
            session['recovery_canton']=consultante.canton
            session['recovery_phone']=consultante.telefono
            tipo=1
        
            return jsonify({
                'success': True,
                'message': 'Usuario validado correctamente',
                'tipo':tipo
            })

        
        terapeuta = Terapeuta.query\
            .filter(Terapeuta.correo == usuario_input)\
            .first()

        if terapeuta:
            
            usuario = Usuario.query.filter(Usuario.idusuario == terapeuta.idusuario).first()
            if not usuario:
                return jsonify({'success': False, 'message': 'Error: Usuario no encontrado'})

            if usuario.estado != 1 and tipo_recuperacion!="1":
                session['recovery_estado'] = usuario.estado
                return jsonify({
                    'success': False,
                    'message': 'Usuario bloqueado. Para reactivar tu cuenta, por favor utiliza la opción de "Recuperar Contraseña" para restablecer tus credenciales.'
                })

           
            session['recovery_tipo_usuario'] = 'terapeuta'  
            session['recovery_idusuario'] = usuario.idusuario
            session['recovery_identificacion'] = terapeuta.identificacion
            session['recovery_tipo'] = tipo_recuperacion
            session['recovery_correo'] = terapeuta.correo  
            session['recovery_nombre'] = terapeuta.nombre
            session['recovery_estado'] = usuario.estado
            session['recovery_usuario'] = usuario.usuario
            session['recovery_codigoprofesional'] = terapeuta.codigoprofesional  
            session['recovery_apellido'] = terapeuta.apellido2
            tipo=2
         
            return jsonify({
                'success': True,
                'message': 'Usuario validado correctamente',
                'tipo':tipo
            })

        return jsonify({
            'success': False, 
            'message': 'El correo electrónico no está asociado a ningún usuario.'
        })
       
    except Exception as e:
       
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500
        
def normalize_text(text):
    if not text:
        return ''
    text = unicodedata.normalize('NFKD', text.strip().lower())
    # Elimina acentos combinados
    return ''.join(c for c in text if not unicodedata.combining(c))
def normalize_date(date_str):
    if not date_str:
        return None
    try:
        # formato que viene del frontend
        return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z").date()
    except ValueError:
        try:
            # formato de la base de datos
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None     
@credential_bp.route('/validate_questions', methods=['POST'])
def ValidateSecurityQuestions():
    try:
        data = request.get_json()
        question1 = data.get('question1')
        answer1 = str(data.get('answer1')).strip()
        tipo = str(data.get('tipouss')).strip()  # "1" = consultante, "2" = terapeuta

        identificacion = session.get('recovery_identificacion')

        if not identificacion:
            return jsonify({'success': False, 'message': 'Sesión no válida o expirada.'}), 401

        # Inicializar contador si no existe
        if 'failed_attempts' not in session:
            session['failed_attempts'] = 0

        is_valid = False

        # --- 🔹 Consultante ---
        if tipo == "1":
            if question1 == "id_digits":
                expected = identificacion[-3:]
                is_valid = (answer1 == expected)
              
            elif question1 == "birthdate":
                expected = normalize_date(str(session.get('recovery_date')))
                answer = normalize_date(answer1)
                is_valid = (answer == expected)
                
            elif question1 == "canton":
                expected = normalize_text(session.get('recovery_canton'))
                answer = normalize_text(answer1)
                is_valid = (answer == expected)
                
            elif question1 == "phone_digits":
                phone = str(session.get('recovery_phone'))
                expected = phone[-3:] if phone else ""
                is_valid = (answer1 == expected)
                

        # --- 🔹 Terapeuta ---
        elif tipo == "2":
            if question1 == "id_digits":
                expected = identificacion[-3:]
                is_valid = (answer1 == expected)
            elif question1 == "M_last_name":
                expected = str(session.get('recovery_apellido')).lower()
                is_valid = (answer1.lower() == expected)
            elif question1 == "code":
                codigo_prof = str(session.get('recovery_codigoprofesional'))
                expected = codigo_prof[-3:] if codigo_prof else ""
                is_valid = (answer1 == expected)

        # --- Ningún tipo válido ---
        else:
            return jsonify({'success': False, 'message': 'Tipo de usuario no válido.'}), 400

        # --- ✅ Si la respuesta es correcta ---
        if is_valid:
            session['security_verified'] = True
            session.pop('failed_attempts', None)
            idusuario = session.get("recovery_idusuario")
            correo = session.get('recovery_correo')
            nombre = session.get('recovery_nombre')

            code = "{:06d}".format(random.randint(0, 999999))
            usuario = Usuario.query.get(idusuario)
            if not usuario:
                return jsonify({'success': False, 'message': 'Usuario no encontrado'})

            usuario.codigo6digitos = code
            db.session.commit()

            # Enviar correo
            email_service.SendVerificationCodeCredentials(
                email=correo,
                username=nombre,
                code=code
            )

            return jsonify({
                'success': True,
                'message': 'Respuesta correcta. Se ha enviado un código de verificación a tu correo.'
            })

        
        session['failed_attempts'] += 1
        if session['failed_attempts'] >= 3:
            return jsonify({
                'success': False,
                'blocked': True,
                'message': 'Has alcanzado el número máximo de intentos. Espera 24 horas para volver a intentarlo.'
            })

        return jsonify({
            'success': False,
            'blocked': False,
            'attempts': session['failed_attempts'],
            'message': 'La respuesta no es correcta. Intenta nuevamente.'
        })

    except Exception as e:
     
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

    
@credential_bp.route('/validate_code', methods=['POST'])
def ValidateCode():
    try:
        data = request.get_json()
        code_entered = data.get('code')
       

        idusuario = session.get('recovery_idusuario')
        tipo_recuperacion = session.get('recovery_tipo')

        

        # Buscar el usuario en la base de datos
        uss = Usuario.query.get(idusuario)
        if not uss:
            return jsonify({'success': False, 'message': 'Usuario no encontrado en el sistema.'})

       

        # Validar código
        if str(uss.codigo6digitos) != str(code_entered):
            return jsonify({'success': False, 'message': 'Código incorrecto. Intenta nuevamente.'})

        # Código correcto → limpiar código para que no se reutilice
        uss.codigo6digitos = None
        db.session.commit()

        
        if tipo_recuperacion == "1":
            session['code_verified'] = True 
            return jsonify({
                'success': True,
                'typw':"1", 
                'redirect_url': url_for('routes.restablecer_contra')
            })

        
        elif tipo_recuperacion == "2":
            correo = session.get("recovery_correo")
            username = uss.usuario  

            session["code"]=code_entered
            email_service.SendUsernameReminder(email=correo,  uss=username)
            registrarAuditoria(
            identificacion_consultante=session.get("idusuario"),
            tipo_actividad=9,  
            descripcion=f"Recuperacion de Usuario",
            codigo=session.get("code"),
            datos_modificados = { "servicio": data.get("tiporegistro", 0),"hora": datetime.now()},
            exito=True
            )
            return jsonify({
                'success': True,
                'typw':"2",                
                'redirect_url': url_for('auth.login'),
                'message': f'Tu nombre de usuario fue enviado a tu correo {correo}.'
            })

        else:
            return jsonify({
                'success': False,
                'message': 'Tipo de recuperación inválido.'
            })

    except Exception as e:
        
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor.'
        }), 500
        
        
        


@credential_bp.route('/update_password', methods=['POST'])
def UpdatePassword():
    try:
        # Validar sesión
        if not session.get('code_verified'):
            return jsonify({'success': False, 'message': 'No autorizado.'}), 403

        data = request.get_json()
        new_password = data.get('new_password')

        if not new_password or len(new_password) < 6:
            return jsonify({'success': False, 'message': 'La contraseña debe tener al menos 6 caracteres.'})

        idusuario = session.get('recovery_idusuario')
        if not idusuario:
            return jsonify({'success': False, 'message': 'Sesión expirada. Inicia el proceso nuevamente.'})

        usuario = Usuario.query.get(idusuario)
        if not usuario:
            return jsonify({'success': False, 'message': 'Usuario no encontrado.'})

        # Obtiene las ultimas 6 contraseñas del historial
        historial = (
            RestriccionPassword.query
            .filter_by(idusuario=idusuario)
            .order_by(RestriccionPassword.fecha_registro.desc())
            .limit(6)
            .all()
            )

        for registro in historial:
           if bcrypt.checkpw(new_password.encode('utf-8'), registro.password_hash.encode('utf-8')):
            return jsonify({
            'success': False,
            'message': 'La nueva contraseña no puede ser igual a las últimas 6 utilizadas.'
        }), 400

        #  Si pasa la validacion actualiza la contraseña
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        usuario.password = hashed_password

        #  Actualiza estado si aplica
        if usuario.estado == 0:
            usuario.estado = 1
            usuario.intentos = 0

        db.session.commit()

        # Registra auditoría
        registrarAuditoria(
            identificacion_consultante=usuario.idusuario,
            tipo_actividad=10,  
            descripcion=f"Cambio de contrasena",
            codigo=session.get("code"),
            datos_modificados = { "servicio": data.get("tiporegistro", 0),"hora": datetime.now()},
            exito=True
            )
        # Limpiar sesión temporal
        session.pop('code_verified', None)

        return jsonify({'success': True, 'message': 'Contraseña actualizada correctamente.'})

    except Exception as e:
       
        return jsonify({'success': False, 'message': 'Error interno del servidor.'}), 500
