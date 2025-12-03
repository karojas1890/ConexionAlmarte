from flask import Blueprint, jsonify, request,send_file
from app.extensions import db
from app.models.encuesta import EncuestaUsabilidad
from io import BytesIO
import pandas as pd
from datetime import datetime

encuesta_bp = Blueprint("encuesta", __name__)

@encuesta_bp.route("/encuesta", methods=["POST"])
def GuardarEncuesta():
    try:
        datos = request.get_json()

        usuario_id = datos.get("usuario_id")
        rol_usuario = datos.get("rol_usuario")
      
        if not usuario_id or not rol_usuario:
            return jsonify({"error": "usuario_id y rol_usuario son obligatorios"}), 400
        
        encuesta = EncuestaUsabilidad(
            usuario_id=usuario_id,
            rol_usuario=rol_usuario,
    
           # Sección 1: Facilidad de Uso
            navegacion_clara=datos.get("navegacion_clara"),
            facil_encontrar_funciones=datos.get("facil_encontrar_funciones"),
            instrucciones_claras=datos.get("instrucciones_claras"),
            aprendizaje_rapido=datos.get("aprendizaje_rapido"),
    
           # Sección 2: Eficiencia
            tareas_rapidas=datos.get("tareas_rapidas"),
            pocos_pasos=datos.get("pocos_pasos"),
            proceso_citas_agil=datos.get("proceso_citas_agil"),
            registro_eficiente=datos.get("registro_eficiente"),
    
           # Sección 3: Atracción
            diseno_atractivo=datos.get("diseno_atractivo"),
            colores_agradables=datos.get("colores_agradables"),
            iconos_modernos=datos.get("iconos_modernos"),  
            aspecto_general=datos.get("aspecto_general"), 
    
          # Sección 4: Inclusivo
            texto_comodo=datos.get("texto_comodo"), 
            contrastes_adecuados=datos.get("contrastes_adecuados"),  
            diseno_inclusivo=datos.get("diseno_inclusivo"),  
            lenguaje_respetuoso=datos.get("lenguaje_respetuoso"), 
    
          # Sección 5: Evitar Frustración
            proteccion_errores=datos.get("proteccion_errores"),  
            mensajes_error_claros=datos.get("mensajes_error_claros"),  
            respuesta_consistente=datos.get("respuesta_consistente"),  
            control_tranquilidad=datos.get("control_tranquilidad"),  
    
        # Sección 6: Satisfacción General
            satisfaccion_general=datos.get("satisfaccion_general"),  
            herramienta_util=datos.get("herramienta_util"),  
            recomendaria_aplicacion=datos.get("recomendaria_aplicacion"), 
            sentir_apoyado=datos.get("sentir_apoyado"),  
    
        # Preguntas Abiertas
            que_mas_gusto=datos.get("que_mas_gusto"),
            que_mejorar=datos.get("que_mejorar"),
            que_confuso_frustrante=datos.get("que_confuso_frustrante")
        )
        
        db.session.add(encuesta)
        db.session.commit()

        return jsonify({"valido":True,"mensaje": "Encuesta guardada exitosamente"}), 201

    except Exception as e:
        print("ERROR GuardarEncuesta:", e)
        return jsonify({"error": "Error al guardar la encuesta"}), 500
    

@encuesta_bp.route("/encuestas", methods=["GET"])
def VerEncuesta():
     
    try:
        encuestas = EncuestaUsabilidad.query.all()
        
        encuestas_data = []
        for encuesta in encuestas:
            encuestas_data.append({
                'id': encuesta.id,
                'usuario_id': encuesta.usuario_id,
                'rol_usuario': encuesta.rol_usuario,
                'fecha_encuesta': encuesta.fecha_encuesta.isoformat() if encuesta.fecha_encuesta else None,
                
                # Mapeo para las preguntas q1-q24 que usa el frontend
                'P1': encuesta.navegacion_clara,
                'P2': encuesta.facil_encontrar_funciones,
                'P3': encuesta.instrucciones_claras,
                'P4': encuesta.aprendizaje_rapido,
                'P5': encuesta.tareas_rapidas,
                'P6': encuesta.pocos_pasos,
                'P7': encuesta.proceso_citas_agil,
                'P8': encuesta.registro_eficiente,
                'P9': encuesta.diseno_atractivo,
                'P10': encuesta.colores_agradables,
                'P11': encuesta.iconos_modernos,
                'P12': encuesta.aspecto_general,
                'P13': encuesta.texto_comodo,
                'P14': encuesta.contrastes_adecuados,
                'P15': encuesta.diseno_inclusivo,
                'P16': encuesta.lenguaje_respetuoso,
                'P17': encuesta.proteccion_errores,
                'P18': encuesta.mensajes_error_claros,
                'P19': encuesta.respuesta_consistente,
                'P20': encuesta.control_tranquilidad,
                'P21': encuesta.satisfaccion_general,
                'P22': encuesta.herramienta_util,
                'P23': encuesta.sentir_apoyado,
                'P24': encuesta.recomendaria_aplicacion,
                
                # Preguntas abiertas
                'open1': encuesta.que_mas_gusto or '',
                'open2': encuesta.que_mejorar or '',
                'open3': encuesta.que_confuso_frustrante or '',
               
                
                # Métricas
                'puntuacion_total': encuesta.puntuacion_total,
                'promedio_seccion': float(encuesta.promedio_seccion) if encuesta.promedio_seccion else 0,
                'completada': encuesta.completada
            })
       
        return jsonify({'success': True, 'encuestas': encuestas_data})
        
    except Exception as e:
        print("ERROR api_encuestas:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

    
@encuesta_bp.route("/exportar", methods=["GET", "POST"])
def ExportarEncuesta():
    try:
        encuestas = EncuestaUsabilidad.query.all()
        
        data = []
        for encuesta in encuestas:
            row = {
                'ID': encuesta.id,
                'Usuario_ID': encuesta.usuario_id,
                'Rol': encuesta.rol_usuario,
                'Fecha': encuesta.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if encuesta.fecha_creacion else '',
                'Puntuacion_Total': encuesta.puntuacion_total or 0,
                'Promedio': float(encuesta.promedio_seccion) if encuesta.promedio_seccion else 0,
                'Completada': 'Sí' if encuesta.completada else 'No',
                
                # Sección 1: Facilidad de Uso
                'Navegacion_Clara': encuesta.navegacion_clara or '',
                'Facil_Encontrar_Funciones': encuesta.facil_encontrar_funciones or '',
                'Instrucciones_Claras': encuesta.instrucciones_claras or '',
                'Aprendizaje_Rapido': encuesta.aprendizaje_rapido or '',
                
                # Sección 2: Eficiencia
                'Tareas_Rapidas': encuesta.tareas_rapidas or '',
                'Pocos_Pasos': encuesta.pocos_pasos or '',
                'Proceso_Citas_Agil': encuesta.proceso_citas_agil or '',
                'Registro_Eficiente': encuesta.registro_eficiente or '',
                
                # Sección 3: Atracción
                'Diseño_Atractivo': encuesta.diseno_atractivo or '',
                'Colores_Agradables': encuesta.colores_agradables or '',
                'Iconos_Modernos': encuesta.iconos_modernos or '',
                'Aspecto_General': encuesta.aspecto_general or '',
                
                # Sección 4: Inclusivo
                'Texto_Comodo': encuesta.texto_comodo or '',
                'Contrastes_Adecuados': encuesta.contrastes_adecuados or '',
                'Diseño_Inclusivo': encuesta.diseno_inclusivo or '',
                'Lenguaje_Respetuoso': encuesta.lenguaje_respetuoso or '',
                
                # Sección 5: Evitar Frustración
                'Proteccion_Errores': encuesta.proteccion_errores or '',
                'Mensajes_Error_Claros': encuesta.mensajes_error_claros or '',
                'Respuesta_Consistente': encuesta.respuesta_consistente or '',
                'Control_Tranquilidad': encuesta.control_tranquilidad or '',
                
                # Sección 6: Satisfacción General
                'Satisfaccion_General': encuesta.satisfaccion_general or '',
                'Herramienta_Util': encuesta.herramienta_util or '',
                'Recomendaria_Aplicacion': encuesta.recomendaria_aplicacion or '',
                'Sentir_Apoyado': encuesta.sentir_apoyado or '',
                
                # Preguntas Abiertas
                'Que_Mas_Gusto': encuesta.que_mas_gusto or '',
                'Que_Mejorar': encuesta.que_mejorar or '',
                'Que_Confuso_Frustrante': encuesta.que_confuso_frustrante or '',
            }
            data.append(row)
        
        # Crear DataFrame
        df = pd.DataFrame(data)
        
        # Crear archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Encuestas_Usabilidad', index=False)
            
            # Obtener workbook y worksheet para formatear
            workbook = writer.book
            worksheet = writer.sheets['Encuestas_Usabilidad']
            
            # Formato para headers
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#5f9ea0',
                'font_color': 'white',
                'border': 1,
                'align': 'center'
            })
            
            # Formato para celdas normales
            cell_format = workbook.add_format({
                'border': 1,
                'align': 'left',
                'valign': 'top'
            })
            
            # Formato para números
            number_format = workbook.add_format({
                'border': 1,
                'align': 'center',
                'valign': 'top'
            })
            
            # Aplicar formatos a los headers
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Ajustar ancho de columnas automáticamente
            for i, col in enumerate(df.columns):
                max_len = max(
                    df[col].astype(str).str.len().max(),
                    len(col)
                ) + 2
                worksheet.set_column(i, i, min(max_len, 30))
            
            # Aplicar formato a las celdas de datos
            for row_num in range(1, len(df) + 1):
                for col_num in range(len(df.columns)):
                    # Aplicar formato de número para las columnas de puntuación
                    if any(keyword in df.columns[col_num].lower() for keyword in ['puntuacion', 'promedio']):
                        worksheet.write(row_num, col_num, df.iloc[row_num-1, col_num], number_format)
                    else:
                        worksheet.write(row_num, col_num, df.iloc[row_num-1, col_num], cell_format)
            
            # Agregar filtros
            worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
            
            # Agregar hoja de resumen
            CrearHojaResumen(workbook, df)
        
        output.seek(0)
        
        # Crear nombre del archivo con fecha
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        nombre_archivo = f'encuestas_usabilidad_{fecha_actual}.xlsx'
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=nombre_archivo
        )
        
    except Exception as e:
        print("ERROR ExportarEncuestas:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

def CrearHojaResumen(workbook, df):
    """Crear hoja de resumen con estadísticas"""
    worksheet = workbook.add_worksheet('Resumen')
    
    # Formato para títulos
    title_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'fg_color': '#34495e',
        'font_color': 'white',
        'border': 1,
        'align': 'center'
    })
    
    # Formato para subtítulos
    subtitle_format = workbook.add_format({
        'bold': True,
        'fg_color': '#5f9ea0',
        'font_color': 'white',
        'border': 1
    })
    
    # Formato para datos
    data_format = workbook.add_format({
        'border': 1,
        'align': 'left'
    })
    
    # Estadísticas básicas
    total_encuestas = len(df)
    promedio_general = df['Promedio'].mean()
    total_pacientes = len(df[df['Rol'] == 'paciente'])
    total_terapeutas = len(df[df['Rol'] == 'terapeuta'])
    
    # Escribir estadísticas
    worksheet.write('A1', 'RESUMEN DE ENCUESTAS DE USABILIDAD', title_format)
    worksheet.merge_range('A1:E1', 'RESUMEN DE ENCUESTAS DE USABILIDAD', title_format)
    
    worksheet.write('A3', 'Estadísticas Generales', subtitle_format)
    worksheet.merge_range('A3:B3', 'Estadísticas Generales', subtitle_format)
    
    datos_resumen = [
        ['Total de Encuestas:', total_encuestas],
        ['Puntuación Promedio:', round(promedio_general, 2)],
        ['Total Pacientes:', total_pacientes],
        ['Total Terapeutas:', total_terapeutas],
        ['Porcentaje Completadas:', f"{(len(df[df['Completada'] == 'Sí']) / total_encuestas * 100):.1f}%"]
    ]
    
    for i, (label, value) in enumerate(datos_resumen, start=4):
        worksheet.write(f'A{i}', label, subtitle_format)
        worksheet.write(f'B{i}', value, data_format)
    
    # Promedios por sección
    worksheet.write('A10', 'Puntuación Promedio por Sección', subtitle_format)
    worksheet.merge_range('A10:B10', 'Puntuación Promedio por Sección', subtitle_format)
    
    secciones = [
        ('Facilidad de Uso', ['Navegacion_Clara', 'Facil_Encontrar_Funciones', 'Instrucciones_Claras', 'Aprendizaje_Rapido']),
        ('Eficiencia', ['Tareas_Rapidas', 'Pocos_Pasos', 'Proceso_Citas_Agil', 'Registro_Eficiente']),
        ('Atracción', ['Diseño_Atractivo', 'Colores_Agradables', 'Iconos_Modernos', 'Aspecto_General']),
        ('Inclusivo', ['Texto_Comodo', 'Contrastes_Adecuados', 'Diseño_Inclusivo', 'Lenguaje_Respetuoso']),
        ('Evitar Frustración', ['Proteccion_Errores', 'Mensajes_Error_Claros', 'Respuesta_Consistente', 'Control_Tranquilidad']),
        ('Satisfacción General', ['Satisfaccion_General', 'Herramienta_Util', 'Recomendaria_Aplicacion', 'Sentir_Apoyado'])
    ]
    
    row_num = 11
    for seccion_nombre, columnas in secciones:
        # Filtrar columnas que existen en el DataFrame
        columnas_existentes = [col for col in columnas if col in df.columns]
        if columnas_existentes:
            promedio_seccion = df[columnas_existentes].mean().mean()
            worksheet.write(f'A{row_num}', seccion_nombre, subtitle_format)
            worksheet.write(f'B{row_num}', round(promedio_seccion, 2), data_format)
            row_num += 1
    
    # Ajustar anchos de columnas
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 15)
    
@encuesta_bp.route("/encuestas/<int:encuesta_id>", methods=["GET"])
def ObtenerEncuestaDetalle(encuesta_id):
    
    try:
        encuesta = EncuestaUsabilidad.query.get_or_404(encuesta_id)
        
        encuesta_data = {
            'id': encuesta.id,
            'usuario_id': encuesta.usuario_id,
            'rol_usuario': encuesta.rol_usuario,
            'fecha_encuesta': encuesta.fecha_encuesta.isoformat() if encuesta.fecha_encuesta else None,
            
            # Sección 1: Facilidad de Uso
            'P1': encuesta.navegacion_clara,
            'P2': encuesta.facil_encontrar_funciones,
            'P3': encuesta.instrucciones_claras,
            'P4': encuesta.aprendizaje_rapido,
            
            # Sección 2: Eficiencia
            'P5': encuesta.tareas_rapidas,
            'P6': encuesta.pocos_pasos,
            'P7': encuesta.proceso_citas_agil,
            'P8': encuesta.registro_eficiente,
            
            # Sección 3: Atracción
            'P9': encuesta.diseno_atractivo,
            'P10': encuesta.colores_agradables,
            'P11': encuesta.iconos_modernos,
            'P12': encuesta.aspecto_general,
            
            # Sección 4: Inclusivo
            'P13': encuesta.texto_comodo,
            'P14': encuesta.contrastes_adecuados,
            'P15': encuesta.diseno_inclusivo,
            'P16': encuesta.lenguaje_respetuoso,
            
            # Sección 5: Evitar Frustración
            'P17': encuesta.proteccion_errores,
            'P18': encuesta.mensajes_error_claros,
            'P19': encuesta.respuesta_consistente,
            'P20': encuesta.control_tranquilidad,
            
            # Sección 6: Satisfacción General
            'P21': encuesta.satisfaccion_general,
            'P22': encuesta.herramienta_util,
            'P23': encuesta.recomendaria_aplicacion,
            'P24': encuesta.sentir_apoyado,
            
            # Preguntas Abiertas
            'que_mas_gusto': encuesta.que_mas_gusto,
            'que_mejorar': encuesta.que_mejorar,
            'que_confuso_frustrante': encuesta.que_confuso_frustrante,
            
            # Métricas
            'puntuacion_total': encuesta.puntuacion_total,
            'promedio_seccion': float(encuesta.promedio_seccion) if encuesta.promedio_seccion else 0,
            'completada': encuesta.completada
        }
        
        return jsonify({'success': True, 'encuesta': encuesta_data})
        
    except Exception as e:
        print("ERROR obtener_encuesta_detalle:", e)
        return jsonify({'success': False, 'error': str(e)}), 500