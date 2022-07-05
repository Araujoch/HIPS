from datetime import datetime
import os


def escribir_log(alarmas_o_prevencion, tipo_alarma, motivo, ip_o_email = ''):
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    lo_escrito = f'{fecha_hora} :: {tipo_alarma} :: {ip_o_email} \t{motivo}'

    if alarmas_o_prevencion == 'alarmas' or alarmas_o_prevencion == 'prevencion':
        os.system(f"sudo echo '{lo_escrito}' >> /var/log/hips/{alarmas_o_prevencion}.log")
    else:
        print("alarmas_o_prevencion tiene que tener el valor de 'alarmas' o 'prevencion' ")