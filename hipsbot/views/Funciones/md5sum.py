
import subprocess
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

    try:
        #Obtenemos los hash que estan almacenamos en la base de datos
        for hash in CheckSuma.objects.raw('SELECT id,directorio,hashsuma FROM hipsbot_checksuma'):

            aux = subprocess.run(['sudo','md5sum',hash.directorio],capture_output=True ).stdout.decode('utf-8')
            
            #Si los hash coinciden no hubo modificacion en el archivo
            if aux == hash.hashsuma:

                modificado = False
                msg = 'No se modifico el directorio : ' + hash.directorio
                listamsg.append(HTML(msg))
            else:
                msg = 'Se modifico el directorio : ' + hash.directorio
                listamsg.append(HTML(msg))
                tipo_alerta = "Alerta"
                asunto      = "Modificacion de archivos binarios!"
                cuerpo      =  tipo_alerta + ' : ' + msg
                func_enviar_mail(asunto,cuerpo)
            
        if modificado:

            msg = "No se modifico ningun directorio "
            listamsg.append(HTML(msg))

    except Exception:
            return "check md5Sum : Hubo un problema al momemnto de ejecutar la accion"
                
    return listamsg