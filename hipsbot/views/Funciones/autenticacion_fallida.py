import os
from hipsbot.views.Herramientas.HTML import HTML
from hipsbot.views.Herramientas.bloquear_usuarios import bloquear_usuario
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail
from hipsbot.views.Herramientas.escribiri_log import escribir_log

'''
    Verificamos en el archivo secure los  intentos fallidos de autenticacion 
    En el caso la cantidad supere 10 intentos,se procede a bloquear temporalmente a ese usuario
'''

def check_autenticacion_fallida():
   
    listamsg = []
    cmd = "sudo cat  /var/log/secure | grep -i 'authentication failure'"
    resultado_cmd = os.popen(cmd).read().split("\n")
    resultado_cmd.pop(-1)

    usuarios_contador = {}

    # Recorremos cada linea de alerta
    for linea in resultado_cmd:
        linea  = linea.split()
        usuario = linea[14].split("=")[1]
        # Si ya esta incializado un contador para el usuario , entonces procedemos, sino, inicializamos
        if usuario in usuarios_contador:
            #si existe le sumamos uno al contador de failure en ese usuario

            usuarios_contador[usuario] = usuarios_contador[usuario] + 1 
           
            # Si el contador de failure del usuario supera un limite, es una alarma,
            
            if usuarios_contador[usuario] == 10:
                #procedemos a bloquear al usario
                bloquear_usuario(usuario)
                msg = f"El usuario : {usuario} fue bloqueado"
                listamsg.append(HTML(msg))
                tipo_alerta = "PREVENCION"
                asunto      = "AUTENTICACION FALLIDA!"
                cuerpo      =  tipo_alerta + ' : ' + msg
                func_enviar_mail(asunto,cuerpo)
                escribir_log(alarmas_o_prevencion='prevencion',
                            tipo_alarma='su:auth_ATTACK',
                            ip_o_email=usuario,
                            motivo='Muchas entradas de auth failure por su:auth por el ruser, se se bloqueo el usuario'
                            )
                msg = f"Demasiados intentos fallidos de iniciar seccion"
                listamsg.append(HTML(msg))
        else:
            usuarios_contador[usuario] = 1
        
    return listamsg