
from flask import Blueprint, request, jsonify,session,url_for
from app.extensions import db
from app.models.consultante import Consultante
from app.models.user import Usuario
from app.models.Terapeuta import Terapeuta
from app.Service import email_service
import random
import bcrypt

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

            if usuario.estado != 1:
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

            print("✅ Usuario validado - Consultante")
            return jsonify({
                'success': True,
                'message': 'Usuario validado correctamente'
            })

        
        terapeuta = Terapeuta.query\
            .filter(Terapeuta.correo == usuario_input)\
            .first()

        if terapeuta:
            
            usuario = Usuario.query.filter(Usuario.idusuario == terapeuta.idusuario).first()
            if not usuario:
                return jsonify({'success': False, 'message': 'Error: Usuario no encontrado'})

            if usuario.estado != 1:
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

            print("✅ Usuario validado - Terapeuta")
            return jsonify({
                'success': True,
                'message': 'Usuario validado correctamente'
            })

        return jsonify({
            'success': False, 
            'message': 'El correo electrónico no está asociado a ningún usuario.'
        })
       
    except Exception as e:
        print(f"Error validando usuario: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500
      
@credential_bp.route('/validate_questions', methods=['POST'])
def ValidateSecurityQuestions():
    try:
        data = request.get_json()
        question1 = data.get('question1')
        answer1 = data.get('answer1')
        print(f"🔍 Validando pregunta: {question1}, respuesta: {answer1}")

        identificacion = session.get('recovery_identificacion')
        print(identificacion)

        # Inicializar contador si no existe
        if 'failed_attempts' not in session:
            session['failed_attempts'] = 0

        is_valid = False

        if question1 == "id_digits":
            expectedAnswer = identificacion[-3:]
            is_valid = answer1 == expectedAnswer
            print(f"{answer1} compare {expectedAnswer}")

        if is_valid:
            session['security_verified'] = True
            session.pop('failed_attempts', None)  # reiniciar contador
            idusuario = session.get("recovery_idusuario")

            correo = session.get('recovery_correo')
            nombre = session.get('recovery_nombre')
            code = "{:06d}".format(random.randint(0, 999999))

            usuario = Usuario.query.get(idusuario)
            if not usuario:
                return jsonify({'success': False, 'message': 'Usuario no encontrado'})

            usuario.codigo6digitos = code
            db.session.commit()

            email_service.SendVerificationCodeCredentials(email=correo, username=nombre, code=code)

            return jsonify({
                'success': True,
                'message': 'Respuestas correctas. Se ha enviado un código de verificación a tu correo.'
            })

        else:
            # Incrementar contador
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
                'message': 'Las respuestas no son correctas. Intenta nuevamente.'
            })

    except Exception as e:
        print(f" Error validando preguntas: {e}")
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500
@credential_bp.route('/validate_code', methods=['POST'])
def ValidateCode():
    try:
        data = request.get_json()
        code_entered = data.get('code')
        print(f"🔐 Validando código ingresado: {code_entered}")

        idusuario = session.get('recovery_idusuario')
        tipo_recuperacion = session.get('recovery_tipo')

        print(tipo_recuperacion)

        # Buscar el usuario en la base de datos
        uss = Usuario.query.get(idusuario)
        if not uss:
            return jsonify({'success': False, 'message': 'Usuario no encontrado en el sistema.'})

        print(f"🧩 Código esperado: {uss.codigo6digitos}")

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
                'redirect_url': url_for('routes.restablecer_contra')
            })

        
        elif tipo_recuperacion == "2":
            correo = session.get("recovery_correo")
            username = uss.usuario  

          
            email_service.SendUsernameReminder(email=correo,  uss=username)

            return jsonify({
                'success': True,
                'redirect_url': url_for('auth.login'),
                'message': f'Tu nombre de usuario fue enviado a tu correo {correo}.'
            })

        else:
            return jsonify({
                'success': False,
                'message': 'Tipo de recuperación inválido.'
            })

    except Exception as e:
        print(f"Error validando código: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor.'
        }), 500
        
        
        
@credential_bp.route('/update_password', methods=['POST'])
def UpdatePassword():
    try:
        
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

        
        usuario.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


        # Si el estado está en 0, actualizarlo a 1
        if usuario.estado == 0:
            usuario.estado = 1

        db.session.commit()

        # Limpiar sesión temporal
        session.pop('code_verified', None)

        return jsonify({'success': True, 'message': 'Contraseña actualizada correctamente.'})

    except Exception as e:
        print(f"❌ Error actualizando contraseña: {e}")
        return jsonify({'success': False, 'message': 'Error interno del servidor.'}), 500