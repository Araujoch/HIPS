import os
import string
import random
import datetime as dt
import sys

from hipsbot.views.Herramientas.HTML import HTML
from hipsbot.views.Herramientas.bloquear_usuarios import bloquear_usuario
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail

def check_ataques_smtp_messages():
    listamsg = []
    cmd = "sudo cat /var/log/messages | grep -i 'service=smtp' | grep -i 'auth failure'"
    resultado_cmd = os.popen(cmd).read().split("\n")
    resultado_cmd.pop(-1)

    usuarios_contador = {}

    # Recorremos cada linea de alerta
    for linea in resultado_cmd:
        linea  = linea.split()
        usuario = linea[9].split("=")[1][:-1]
        
        # Si ya esta incializado un contador para el usuario en username, entonces procedemos, sino, inicializamos
        if usuario in usuarios_contador:
            usuarios_contador[usuario] = usuarios_contador[usuario] + 1 # si existe le sumamos uno al contador de failure en ese usuario
            # Si el contador de failure del usuario supera un limite, es una alarma, procedemos a cambiar la contrasenha
            if usuarios_contador[usuario] == 50:
                #procedemos a bloquar al usuario
                bloquear_usuario(usuario)

                msg = f"El usuario : {usuario} fue bloqueado"
                listamsg.append(HTML(msg))
                tipo_alerta = "PREVENCION"
                asunto      = "Ataque SMTP!"
                cuerpo      =  tipo_alerta + ' : ' + msg
                func_enviar_mail(asunto,cuerpo)
                msg = f"Muchas entradas de auth failure de stmp en el archivo /var/log/messages"
                listamsg.append(HTML(msg))
               
        else:
            usuarios_contador[usuario] = 1
    if len(listamsg) is None :
        msg = "No se registraron ataques SMTP "
        listamsg.append(HTML(msg))
    return listamsg
        
