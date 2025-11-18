from flask import Blueprint, render_template, send_from_directory, current_app,url_for,redirect,session
import os
from .decorators import loginRequired,rolRequired,codeVerifiedRequired

routes_bp = Blueprint("routes", __name__)



@routes_bp.route('/')
def index():
    return render_template('login.html')

@routes_bp.route('/service-worker.js')
def service_worker():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'service-worker.js')

@routes_bp.route("/dashboard_Consultante", endpoint="dashboard_Consultante")
@rolRequired(1,3,4)
@loginRequired
def DashboardPrincipal():
    return render_template("dashboard-Consultante.html")

@routes_bp.route("/codigo_restablecer", endpoint="codigo_restablecer")
def CodigoRestablecer():
    return render_template("codigo-restablecer.html")


@routes_bp.route("/preguntas_seguridad",endpoint="preguntas_seguridad")
def PreguntaSeguridad():
    return render_template("pregunta-seguridad.html")
    

@routes_bp.route("/verificar_Codigo", endpoint="verificar_Codigo")
#decorador para proteccion de las paginas
@loginRequired 
def verificar_Codigo():
    if "rol" not in session:
        return redirect(url_for("auth.login"))

    
    if session["rol"] == 1:  # tipo 1 = consultante
        dashboard_url = url_for("routes.dashboard_Consultante")
    elif session["rol"] == 2:  # tipo 2 = terapeuta
        dashboard_url = url_for("routes.dashboard")
    elif session["rol"]==3 or session["rol"]==4:
       dashboard_url= url_for("routes.quien_eres")
    return render_template("VerificarCodigo.html", dashboard_url=dashboard_url)

# @routes_bp.route("/Tipo_Cambios", endpoint="Tipo_Cambios")
# def TipoCambio():
#     return render_template("tipoCambios.html")

@routes_bp.route("/diary", endpoint="diary")
@rolRequired(1,3,4)
@loginRequired 
def Diary():
    return render_template("diary.html")

@routes_bp.route("/audit_P", endpoint="audit_P")
@rolRequired(1,3)
@loginRequired 
def Diary():
    return render_template("patientLogs.html")

@routes_bp.route("/sig_up", endpoint="sig_up")
def SigUp():
    return render_template("sig-up.html")


@routes_bp.route("/acerca_de", endpoint="acerca_de")
def AcercaDe():
    return render_template("acercaDe.html")


@routes_bp.route("/restablecer_contra", endpoint="restablecer_contra")
@codeVerifiedRequired
def RestablecerCOntrasena():
    return render_template("restablecer-contrasena.html")

@routes_bp.route("/pme_manage", endpoint="pme_manage")
@rolRequired(3)
@loginRequired 
def ManagementPME():
    return render_template("pme-management.html")


@routes_bp.route("/add_card", endpoint="add_card")
@rolRequired(1,3)
@loginRequired 
def AddCard():
    return render_template("add-card.html")



@routes_bp.route("/search_therapist", endpoint="search_therapist")
def SearchTherapist():
    return render_template("searchTherapist.html")


@routes_bp.route("/use_card", endpoint="use_card")
@rolRequired(1,3)
@loginRequired 
def UseCard():
    return render_template("usar-tarjetas.html")

@routes_bp.route("/patient_activity", endpoint="patient_activity")
@rolRequired(1,3)
@loginRequired
def PatientActivity():
    return render_template("patient-activity.html")


@routes_bp.route("/auditor", endpoint="auditor")
@rolRequired(2)
@loginRequired
def Auditoria():
    return render_template("audit-log.html")

@routes_bp.route("/pme_add", endpoint="pme_add")
@rolRequired(3)
@loginRequired 
def AddPME():
    return render_template("pme-add.html")

@routes_bp.route("/recuperar_Contra", endpoint="recuperar_Contra")
def RecuperarContrasena():
    return render_template("recuperar-Contrasena.html")


@routes_bp.route("/diary_trygger", endpoint="diary_trygger")
@rolRequired(1,3,4)
@loginRequired 
def DiaryTrygger():
    return render_template("diary-trygger.html")

@routes_bp.route("/diary_progress", endpoint="diary_progess")
@rolRequired(1,3,4)
@loginRequired
def DiaryProgress():
    return render_template("diary-progress.html")



@routes_bp.route("/tools_progress", endpoint="tools_progress")
@rolRequired(1,3,4)
@loginRequired 
def ToolsProgress():
    return render_template("tool-progress.html")

@routes_bp.route("/tools_usage", endpoint="tools_usage")
@rolRequired(1,3,4)
@loginRequired 
def ToolsUsage():
    return render_template("tools-usage.html")

@routes_bp.route("/profile", endpoint="profile")
@rolRequired(1,3,4)
@loginRequired 
def Profile():
    return render_template("profile.html")

@routes_bp.route("/payment",endpoint="payment")
@rolRequired(1,3)
@loginRequired
def Payment():
    return render_template("payment-form.html")

@routes_bp.route("/select_Service",endpoint="select_Service")
@rolRequired(1,3)
@loginRequired
def Service():
    return render_template("select-service.html")

@routes_bp.route("/select_datetime",endpoint="select_datetime")
@rolRequired(1,3)
@loginRequired
def Datetime():
    return render_template("select-datetime.html")

@routes_bp.route("/payment_summary", endpoint="payment_summary")
@rolRequired(1,3)
@loginRequired
def PaymentSummary():
    return render_template("payment-summary.html")

@routes_bp.route("/tools_details", endpoint="tools_details")
@rolRequired(1,3,4)
@loginRequired
def ToolsDetails():
    return render_template("tools-details.html")

@routes_bp.route("/tools_Menu", endpoint="tools_Menu")
@rolRequired(1,3,4)
@loginRequired
def ToolsMe():
    return render_template("toolsMenu.html")

#url terapeuta
@routes_bp.route("/dashboard", endpoint="dashboard")
@rolRequired(2)
@loginRequired
def ToolsMe():
    return render_template("dashboardTerapeuta.html")
                         
@routes_bp.route("/mi_agenda", endpoint="mi_agenda")
@rolRequired(2)
@loginRequired
def MiAgenda():
    return render_template("mi-agenda.html")


@routes_bp.route("/availability", endpoint="availability")
@rolRequired(2)
@loginRequired
def Availability():
    return render_template("availability.html")


@routes_bp.route("/quien_eres", endpoint="quien_eres")
@rolRequired(3,4)
@loginRequired
def QuienEres():
    return render_template("quien-Eres.html")


@routes_bp.route("/gestionar_pacientes", endpoint="gestionar_pacientes")
@rolRequired(2)
@loginRequired
def GestionarPacientes():
    return render_template("gestionarPacientes.html")

    
    
@routes_bp.route("/provincia", endpoint="provincia")
def Provincia():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'geoBoundaries-CRI-ADM1_simplified.geojson')

@routes_bp.route("/canton", endpoint="canton")
def Canton():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'geoBoundaries-CRI-ADM2_simplified.geojson')

@routes_bp.route("/distrito", endpoint="distrito")
def Provincia():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'geoBoundaries-CRI-ADM3_simplified.geojson')

       
        
    