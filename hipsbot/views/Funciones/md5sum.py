
import subprocess
from hipsbot.models import CheckSuma
from hipsbot.views.Herramientas.HTML import HTML


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
            
        if modificado:

            msg = "No se modifico ningun directorio "
            listamsg.append(HTML(msg))

    except Exception:
            return "check md5Sum : Hubo un problema al momemnto de ejecutar la accion"
                
    return listamsg