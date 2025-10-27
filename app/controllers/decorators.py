from functools import wraps
from flask import session, redirect, url_for, flash , request


#este metodo se usa para que si no se ha incioado sesion no se pueda navegar por las paginas 
def loginRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #valida si existe una sesion con ese nombre sino lo envia al login 
        if "usuario" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def rolRequired(*roles):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_rol = session.get('rol')
            if user_rol not in roles:
                flash("No está autorizado para ingresar a esta vista.", "warning")
                if user_rol in [1, 3, 4]:
                    return redirect(request.referrer or url_for('routes.index'))
                elif user_rol == 2:
                    return redirect(request.referrer or url_for('routes.dashboard'))
            return func(*args, **kwargs)
        return wrapper
    return decorador

def codeVerifiedRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('code_verified'):
            flash("Debes realizar el procesos de seguridad antes de ir a esta vista.", "warning")
            return redirect(url_for('auth.login'))  
        return f(*args, **kwargs)
    return decorated_function