import os
from hipsbot.views.Herramientas.HTML import HTML
from hipsbot.views.Herramientas.bloquear_ip import bloquear_ip
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail
from hipsbot.views.Herramientas.escribiri_log import escribir_log

'''
    Verifica archivo access.log y bloquea todas las ip cuyas solititudes terminen en 404 {page not found}

    cat                         =
    /var/log/httpd/access.log   =
    | grep -i 'HTTP'            =
    | grep -i '404'             =
'''
def check_access_log():
    listamsg = []
    cmd = "sudo cat /var/log/httpd/access_log | grep -i 'HTTP' | grep -i '404'"
    resultado_cmd = os.popen(cmd).read().split('\n')
    resultado_cmd.pop(-1)

    contador_ip = {}

    for linea in resultado_cmd:
        ip =  linea.split()[0]
        
        if ip in contador_ip:
            contador_ip[ip] = contador_ip[ip] + 1
            if contador_ip[ip] == 5:
                msg = f"{ip} : bloqueada muchos respuestas 404 desde esta IP "
                listamsg.append(HTML(msg))
                tipo_alerta = "PREVENCION"
                asunto      = "MASIVOS 404!"
                cuerpo      =  tipo_alerta + ' : ' + msg
                func_enviar_mail(asunto,cuerpo)
                escribir_log(
                            alarmas_o_prevencion='prevencion',
                            tipo_alarma='MASIVOS 404',
                            ip_o_email=ip, motivo='Se registraron muchas respuestas 404 desde la misma IP, se bloqueo el IP'
                            )
                # bloqueamos la ip
                bloquear_ip(ip)  
                
        else:
            contador_ip[ip] = 1

    return listamsg
