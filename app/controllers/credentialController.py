
from flask import Blueprint, request, jsonify,session
from app.extensions import db
from app.models.consultante import Consultante
from app.models.user import Usuario
from app.models.Terapeuta import Terapeuta
from app.Service import email_service
import random

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
        print(f"❌ Error validando usuario: {e}")
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
        #debug
        print(f"🔍 Validando pregunta: {question1}, respuesta: {answer1}")

       
        if 'recovery_idconsultante' not in session:
            return jsonify({'success': False, 'message': 'Sesión expirada'})

       
       
        idusuario = session.get('recovery_idusuario')
       

     
        is_valid = False
        
        if question1 == 'id_digits':
           
            expected_answer = idusuario[-4:]
            is_valid = answer1 == expected_answer
           
        
    

        if is_valid:
            
            session['security_verified'] = True
            
            tipo_recuperacion=session.get("tipo")
            if tipo_recuperacion == '1':  
                tipo_actividad = 10  
                descripcion = "Código para recuperación de contraseña"
            elif tipo_recuperacion == '2':  
                tipo_actividad = 9   
                descripcion = "Código para recuperación de usuario"
            
            correo = session.get('recovery_correo')
            nombre = session.get('recovery_nombre')
            
            code="{:06d}".format(random.randint(0, 999999))
            
            usuario = Usuario.query.get(idusuario)
            usuario.codigo6digitos = code
            db.session.commit()
            
           
            
            email_service.SendVerificationCodeCredentials( email=correo,username=nombre,code=code)
            
            return jsonify({
                'success': True,
                'message': 'Respuestas correctas. Se ha enviado un código de verificación a tu correo.'
            })
        else:
            
            return jsonify({
                'success': False, 
                'message': 'Las respuestas no son correctas. Por seguridad, deberás esperar 24 horas para intentarlo nuevamente.'
            })

    except Exception as e:
        print(f"❌ Error validando preguntas: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500
    