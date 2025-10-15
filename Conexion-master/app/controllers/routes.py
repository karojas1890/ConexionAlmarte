from flask import Blueprint, render_template, send_from_directory, current_app
import os

routes_bp = Blueprint("routes", __name__)



@routes_bp.route('/')
def index():
    return render_template('login.html')

@routes_bp.route('/service-worker.js')
def service_worker():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'service-worker.js')

@routes_bp.route("/dashboard", endpoint="dashboard")
def DashboardPrincipal():
    return render_template("dashboard.html")

@routes_bp.route("/verificar_Codigo", endpoint="verificar_Codigo")
def VericarCodigo():
    return render_template("VerificarCodigo.html")

# @routes_bp.route("/Tipo_Cambios", endpoint="Tipo_Cambios")
# def TipoCambio():
#     return render_template("tipoCambios.html")

@routes_bp.route("/payment",endpoint="payment")
def Payment():
    return render_template("payment-form.html")

@routes_bp.route("/select_Service",endpoint="select_Service")
def Service():
    return render_template("select-service.html")

@routes_bp.route("/select_datetime",endpoint="select_datetime")
def Datetime():
    return render_template("select-datetime.html")

@routes_bp.route("/payment_summary", endpoint="payment_summary")
def PaymentSummary():
    return render_template("payment-summary.html")

@routes_bp.route("/tools_details", endpoint="tools_details")
def ToolsDetails():
    return render_template("tools-details.html")

@routes_bp.route("/tools_Menu", endpoint="tools_Menu")
def ToolsMe():
    return render_template("toolsMenu.html")


