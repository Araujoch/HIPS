import os
from hipsbot.views.Herramientas.HTML import HTML

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

    else:
        msg = 'no se encontraron muchos mails en la cola'
    listamsg.append(HTML(msg))
    return listamsg