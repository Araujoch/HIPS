import os
from hipsbot.views.Herramientas.HTML import HTML
from hipsbot.views.Herramientas.cuarentena import cuarentena
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail
from hipsbot.views.Herramientas.matar_proceso import kill_proceso
from hipsbot.views.Herramientas.verificar_libreria import verificar_libreria
'''
    Verifica si exiten herramientas sniffer ejecutandose
    Si exiten verificamos que solo los usuarios permitidos las esten usando
    Si no son usuarios permitidos matamos el proceso y las ponemos en cuarentena
'''

def check_sniffer():
    listamsg = []
    LISTA_NEGRA_HERRAMIENTAS_SNIFFER = ['tcpdump','ethereal', 'wireshark' ,'Ngrep' ,'Snort','Nwatch','Ethereal','Kismet']
    LISTA_NEGRA_LIBRERIAS =['libpcat']
    USUARIOS_PERMITIDOS_SNIFFER = ['root']
    for herramienta in LISTA_NEGRA_HERRAMIENTAS_SNIFFER:
        #Grep busca en el retorno de ps-aux ,quitando todos las lineas donde el usuario llama al proceso 
        cmd = f"ps -aux | grep {herramienta} | grep -v grep | awk '{{print $1, $2, $NF}}'"
        resultado_cmd = os.popen(cmd).read().split('\n')
        resultado_cmd.pop(-1)
        
        for resultado in resultado_cmd:
            lista_resultado = resultado.split(" ")
            #Diccionario de procesos
            #Usuario
            #PID
            #Nombre del programa
            proceso = {"USER": lista_resultado[0],"PID": lista_resultado[1],"PROGRAMA": lista_resultado[2]}
            if resultado != "":
                contador = 0

                for usuario in USUARIOS_PERMITIDOS_SNIFFER:
                    if usuario.lower() == proceso['USER'].lower():
                        proceso["HABILITADO"] = "SI"
                        msg = f"Se detecto una herramienta Sniffer: '{herramienta}' "
                        listamsg.append(HTML(msg))
                        msg = f"pero el usuario: {usuario} esta habilitado para usarla"
                        listamsg.append(HTML(msg))
                    else:
                        contador +=1
                if contador == len(USUARIOS_PERMITIDOS_SNIFFER):
                    proceso["HABILITADO"] = "NO"
                    msg = f"El usuario : '{proceso['USER']}' esta ejecutando la herramienta Sniffer : '{herramienta}' "
                    tipo_alerta = "PREVENCION"
                    asunto      = "SE ENCONTRO HERRAMIENTA SNIFFER!"
                    cuerpo      =  tipo_alerta + ' : ' + msg 
                    func_enviar_mail(asunto,cuerpo)
                    listamsg.append(HTML(msg))
                    msg = f"Pero este usuario: '{proceso['USER']}' no se encuentra en la lista de permitidos"
                    listamsg.append(HTML(msg))
                    msg = f"Se procedera a matar el proceso y la herramienta Sniffer sera puesta en cuarentena ..."
                    listamsg.append(HTML(msg))
                    
                    proceso["USA LIBRERIA SNIFFER"] = verificar_libreria(proceso["PID"])
                    
                    #kill_proceso(proceso["PID"])
    if not len(listamsg):
        msg = "No se encontro ninguna Herramienta Sniffer"
        listamsg.append(HTML(msg))
        
    return listamsg