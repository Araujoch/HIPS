import os
import sys
from hipsbot.views.Herramientas.HTML import HTML

from hipsbot.views.Herramientas.bloquear_ip import bloquear_ip
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail
'''

'''
def ataque_ddos_dns():
    listamsg = []
    dns_file_log = os.popen("sudo cat /descargas/tcpdump_dns").read().split('\n')
    dns_file_log.pop(-1)

    ip_contador = {}

    for elemento_linea in dns_file_log:
        ip_atacante = elemento_linea.split()[2]
        ip_destino = elemento_linea.split()[4][:-1] # [:-1] para borrar el : final

        if (ip_atacante, ip_destino) in ip_contador:
            ip_contador[(ip_atacante, ip_destino)] = ip_contador[(ip_atacante, ip_destino)] + 1

            # Si hubieron al menos 10 ip atacante a un mismo ip destino, entonces es alarmante y tomamos una accion
            if ip_contador[(ip_atacante, ip_destino)] == 10:
            
                # Le damos formato para que acepte iptables
                ip_atacante_iptables = ip_atacante.split('.')[:-1]
                ip_atacante_iptables = f"{ip_atacante_iptables[0]}.{ip_atacante_iptables[1]}.{ip_atacante_iptables[2]}.{ip_atacante_iptables[3]}"
                #Bloqueamos la IP atacante
                
                bloquear_ip(ip_atacante_iptables) 
                msg = f"IP : {ip_atacante} bloqueada posible ataque DDOS"
                listamsg.append(HTML(msg))
                tipo_alerta = "PREVENCION"
                asunto      = "Ataque DDOS!"
                cuerpo      =  tipo_alerta + ' : ' + msg
                func_enviar_mail(asunto,cuerpo)
                msg = f"El administrador fue notificado via mail "
                listamsg.append(HTML(msg))
                

        else:
            ip_contador[(ip_atacante, ip_destino)] = 1
    if len(listamsg) is None:
        msg = "No se registraron ataques DDOS"
    return listamsg