
import subprocess
import os
from hipsbot.models import CheckSuma
from hipsbot.views.Herramientas.HTML import HTML
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail


'''
    Verifica si los archivos binarios del sistema han sido modificados
    Los compara con los hash que estan almacenados en la base de datos
'''


def check_md5sum():

    modificado = True
    listamsg= []

    for hash in CheckSuma.objects.raw('SELECT id,directorio,hashsuma FROM hipsbot_checksuma'):
        aux = os.popen(f"md5sum {hash.directorio}").read()
        print(aux)
        #Si los hash coinciden no hubo modificacion en el archivo
        if aux == hash.hashsuma:
            print(aux)
            print(hash.hashsuma)

            modificado = False
            msg = 'No se modifico el directorio : ' + hash.directorio
            listamsg.append(HTML(msg))
        else:
            if aux != '':
                msg = 'Se modifico el directorio : ' + hash.directorio
                listamsg.append(HTML(msg))
                tipo_alerta = "Alerta"
                asunto      = "Modificacion de archivos binarios!"
                cuerpo      =  tipo_alerta + ' : ' + msg
                func_enviar_mail(asunto,cuerpo)
        
    if modificado:

        msg = "No se modifico ningun directorio "
        listamsg.append(HTML(msg))

                
    return listamsg
