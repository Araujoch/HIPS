import os

from hipsbot.views.Herramientas.HTML import HTML
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail

# Verificamos en todos los usuarios si tienen tareas ejecutandose como cron
def verificar_cronjobs():
    listamsg = []
    #obtenemos lista de usuario:x:0:0:grupo: etc
    usuarios_infos = os.popen("sudo cat /etc/passwd").read().split('\n') 
    usuarios_infos.pop(-1)
    
    # Recorremos cada informacion de un usuario
    for usuario_info in usuarios_infos:
        usuario = usuario_info.split(':')[0] # Obtenemos el usuario
        
        tareas_cron = [] 
        # Verificamos si el usuario tiene tareas en cron
        try:
            tareas_cron = os.popen(f"sudo crontab -l -u {usuario}").read().split('\n')
            tareas_cron.pop(-1)
        except Exception:
            pass
        
        # Si el usuario tiene tareas_cron entonces recorremos cada tarea
        if tareas_cron:
            for tarea_cron in tareas_cron:
                #Obtenemos solo el archivo que se esta ejecutando como cron
                file_script =  tarea_cron.split()[-1]
                msg = f"El usuario {usuario} esta ejecutando el archivo {file_script} con cron"
                listamsg.append(HTML(msg))
                tipo_alerta = "PREVENCION"
                asunto      = "CRONJOBS!"
                cuerpo      =  tipo_alerta + ' : ' + msg
                func_enviar_mail(asunto,cuerpo)
    if (listamsg) in None:    
        msg = "No se encontro niguna tarea como cron."
        listamsg.append(HTML(msg))
    return listamsg
   
