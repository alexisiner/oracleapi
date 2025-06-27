import cx_Oracle
import requests
from typing import Optional, List

def enviar_correo(subject, content_html, mail):
    url = "https://sddsservices.impi.gob.mx/ApiServicios/api/Mail/sendmail"
    
    dsn = cx_Oracle.makedsn("192.168.10.13", "1522", sid="pit")
    conn = cx_Oracle.connect(user="SolicitudesDG", password="Dle$b4Zm", dsn=dsn)

    cursor = conn.cursor()
    
    out_cursor = cursor.var(cx_Oracle.CURSOR)
    cursor.callproc("GET_CORREO_ADMIN", [out_cursor, "cddem6"])
    
    result_cursor = out_cursor.getvalue()
    if result_cursor:
        for row in result_cursor:
            mailFrom = row[0]
            password = row[1]
            user = row[2]

    mail_data = {
        "subject": subject,
        "contentHtml": content_html,
        "mail": mail,
        "mailCCO": None,
        "saveCopy": False,
        "account": {
            "mail": mailFrom,
            "user": user,
            "password": password
        }
    }
    
    try:
        response = requests.post(
            url,
            json=mail_data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
        )
        
        if response.status_code == 200:
            return True
        else:
            return False
            
    except Exception as e:
        return False

def ejecutar_sp(sp_name, params=None):
    dsn = cx_Oracle.makedsn("192.168.10.13", "1522", sid="pit")
    conn = cx_Oracle.connect(user="SolicitudesDG", password="Dle$b4Zm", dsn=dsn)
    
    try:
        cursor = conn.cursor()
        
        out_cursor = cursor.var(cx_Oracle.CURSOR)
        
        cursor.callproc(sp_name, [out_cursor])
        
        result_cursor = out_cursor.getvalue()
        if result_cursor:
            for row in result_cursor:
                folio = row[0]
                asignadoA = row[1]
                estatus = row[2]
                fechaSolicitud = row[3]
                fechaAsignado = row[4]
                AsignadoPor = row[6]
                asunto = row[7]
                nombre = row[8]
                telefono = row[9]
                correo = row[10]
                resumen = row[11]
                nombreAP = row[12]
                nombreAsignadoA = row[13]

                html_content = obtener_html(nombreAP,folio,fechaSolicitud,fechaAsignado,asunto,nombre,telefono,correo,resumen)
                enviar_correo("Solicitud atrasada", html_content, AsignadoPor) #correo para AA

                html_content = obtener_html(nombreAsignadoA,folio,fechaSolicitud,fechaAsignado,asunto,nombre,telefono,correo,resumen)
                enviar_correo("Solicitud atrasada", html_content, correo) #correo para persona asignada

                
    except cx_Oracle.DatabaseError as e:
        error, = e.args
    finally:
        cursor.close()
        conn.close()

def obtener_html(nombreto,folio,fechaSolicitud,fechaAsignado,asunto,nombre,telefono,correo,resumen):
    return f"""
                                    <html>
                                    <head>
                                        <style>
                                            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                                            .header {{ color: black; font-size: 18px; }}
                                            .info-table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
                                            .info-table th {{ background-color: #611232 !important; color: white; text-align: left; padding: 8px; }}
                                            .info-table td {{ padding: 8px; border: 1px solid #ddd; }}
                                            .highlight {{ background-color: #f2f2f2; }}
                                            .footer {{ margin-top: 20px; font-size: 14px; color: #555; }}
                                            .portal-link {{ margin: 15px 0; }}
                                        </style>
                                    </head>
                                    <body>
                                        <p class='header'>Estimad@ {nombreto}:</p>

                                        <p>La siguiente solicitud tiene mas de 15 sin ser atendida:</p>

                                        <table class='info-table'>
                                            <tr>
                                                <th colspan='2'>Información de la Solicitud</th>
                                            </tr>
                                            <tr>
                                                <td width='30%'><strong>Número de Folio</strong></td>
                                                <td class='highlight'>{folio}</td>
                                            </tr>
                                            <tr>
                                                <td><strong>Fecha de Solicitud</strong></td>
                                                <td>{fechaSolicitud.strftime('%d/%m/%Y %H:%M') if fechaSolicitud else 'No especificada'}</td>
                                            </tr>
                                            <tr>
                                                <td><strong>Fecha de Asignación</strong></td>
                                                <td>{fechaAsignado.strftime('%d/%m/%Y %H:%M') if fechaAsignado else 'No especificada'}</td>
                                            </tr>
                                            <tr>
                                                <td><strong>Asunto</strong></td>
                                                <td class='highlight'>{asunto}</td>
                                            </tr>
                                        </table>

                                        <table class='info-table'>
                                            <tr>
                                                <th>Información del Solicitante</th>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <p><strong>Nombre:</strong> {nombre}</p>
                                                    <p><strong>Teléfono:</strong> {telefono}</p>
                                                    <p><strong>Correo electrónico:</strong> {correo}</p>
                                                </td>
                                            </tr>
                                        </table>  

                                        <table class='info-table'>
                                            <tr>
                                                <th>Resumen de la Solicitud:</th>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <p><strong>{resumen}</strong></p>
                                                </td>
                                            </tr>
                                        </table>
                                                                                
                                        <div class="portal-link">
                                            <p>Puede ingresar al portal para su revisión: <a href="https://solicitudesdg.impi.gob.mx/tablero?folio={folio}">https://solicitudesdg.impi.gob.mx/</a></p>
                                        </div>
                                        
                                        <div class='footer'>
                                            <p>Este es un mensaje generado automáticamente. Por favor no responda directamente a este correo.</p>
                                            <p>Para cualquier aclaración, puede contactar al área correspondiente.</p>
                                        </div>
                                    </body>
                                    </html>
                                    """

# Uso correcto:
ejecutar_sp("PKG_SOLICITUDESDG.sp_get_solicitudes_retrasadas")

