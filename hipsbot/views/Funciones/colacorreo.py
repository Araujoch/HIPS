import os
from hipsbot.views.Herramientas.HTML import HTML
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail
from hipsbot.views.Herramientas.escribiri_log import escribir_log

def check_cola_correo():
    listamsg = []
    cmd = "mailq"
    resultado_cmd = os.popen(cmd).read()
    
    if "queue is empty" in resultado_cmd:
       
        msg = 'La cola esta vacia'
        listamsg.append(HTML(msg))
    else:
        resultado = resultado_cmd.splitlines()

    mail_queue = resultado_cmd.splitlines()
    
    if len(mail_queue) > 100:
        msg = "Se encontraron muchos mails en la cola, se aviso al administrador"
        listamsg.append(HTML(msg))
        escribir_log(alarmas_o_prevencion='alarmas',
                    tipo_alarma='COLA_MAIL',
                    motivo='Se detecto muchos mails en la cola')
        func_enviar_mail(tipo_alerta='ALERTA!', asunto='MAIL QUEUE', cuerpo=f'se encontraron {len(mail_queue)} mails en la cola')

    else:
        msg = 'no se encontraron muchos mails en la cola'
        listamsg.append(HTML(msg))
    return listamsg