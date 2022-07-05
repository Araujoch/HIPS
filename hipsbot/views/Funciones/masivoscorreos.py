import os
from hipsbot.views.Herramientas.HTML import HTML
from hipsbot.views.Herramientas.bloquear_ip import bloquear_ip
from hipsbot.views.Herramientas.bloquearmail import bloquear_email
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail
from hipsbot.views.Herramientas.escribiri_log import escribir_log

'''
    Verifica archivo access.log y bloquea todas las ip cuyas solititudes terminen en 404 {page not found}

    cat                         =
    /var/log/httpd/access.log   =
    | grep -i 'HTTP'            =
    | grep -i '404'             =
'''
def check_masivos_mail():
    listamsg = []
    cmd = "sudo cat /var/log/maillog | grep -i 'authid' "
    resultado_cmd = os.popen(cmd).read().split('\n')
    resultado_cmd.pop(-1)

    contador_email = {}

    for linea in resultado_cmd:
        authid = [word for word in linea.split() if 'authid=' in word][0]
        email = authid.split("=")[-1][:-1]
        if email in contador_email:
            # Incrementamos el contador de cuantos email lleva este email
            contador_email[email] = contador_email[email] + 1
            # Si el email envio mas de 50 mails, lo consideramos masivos
            if contador_email[email] == 50:  
                
                bloquear_email(email)
                msg = f"El email : {email} fue bloqueado "
                listamsg.append(HTML(msg))
                tipo_alerta = "PREVENCION"
                asunto      = "MASIVOS CORREOS!"
                cuerpo      =  tipo_alerta + ' : ' + msg
                func_enviar_mail(asunto,cuerpo)
                escribir_log(alarmas_o_prevencion='prevencion',
                            tipo_alarma='Email Bomb',
                            ip_o_email=email,
                            motivo='Se registraron muchos mails por parte de este email, se paso a bloquear el email.'
                            )
                msg = f"Demasiados mail enviados desde un mismo email"
                listamsg.append(HTML(msg))
            
        else:
            contador_email[email] = 1

    return listamsg