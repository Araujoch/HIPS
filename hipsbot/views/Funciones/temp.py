import os

import sys
from hipsbot.views.Herramientas.HTML import HTML
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail

from hipsbot.views.Herramientas.escribiri_log import escribir_log

# Verificamos si hay archivos en /tmp que contengan al comienzo #!
def verificar_script():
    listamsg = []
    # buscamos en el directorio tmp los archivos, y solo queremos lo que son archivos y no directorios (type -f)
    command = f"sudo find /tmp 2>/dev/null -type f" 
    archivos = os.popen(command).read().split()
    
    archivos_a_cuarentena = []
    # Procedemos a verificar los archivos
    for archivo in archivos:
        new_diccionary = {}
        
        # Si el archivo es un py, cpp, c, exe, sh, ruby, php, entra en el if
        if any(substring in archivo for substring in [".cpp", ".py", ".c", ".exe", ".sh", ".ruby", ".php"]):
            new_diccionary['ruta_archivo'] = archivo
            new_diccionary['ruta_a_mover'] = "/cuarentena/tmp_scripts/" + archivo[1:].replace("/", "-")
            new_diccionary['motivo'] = "Es un archivo tipo con extension sospechosa (.py .sh etc)"
            archivos_a_cuarentena.append(new_diccionary)
            msg =  f"\nSe encontro un archivo de tipo script {new_diccionary['ruta_archivo']} (#! primera linea), se movio a cuarentena\n"
            listamsg.append(HTML(msg))
            #cuerpo_email = cuerpo_email + f"\nSe encontro el archivo {new_diccionary['ruta_archivo']} con extension sospechosa (.py, .sh, etc), se envio a cuarentena.\n"
            
        else: 
            # Si no, busca si el archivo tiene un #! en la primera linea, lo cual significa que es un archivo script
            try:     
                with open(f"{archivo}", "r") as f:
                    primera_linea = f.readline() # Leemos la primera linea del archivo
                    if "#!" in primera_linea:
                        new_diccionary['ruta_archivo'] = archivo
                        new_diccionary['ruta_a_mover'] = "/cuarentena/tmp_scripts/" + archivo[1:].replace("/", "-")
                        new_diccionary['motivo'] = "Es un archivo tipo script (#!)"
                        archivos_a_cuarentena.append(new_diccionary)
                        msg =  f"\nSe encontro un archivo de tipo script {new_diccionary['ruta_archivo']} (#! primera linea), se movio a cuarentena\n"
                        listamsg.append(HTML(msg))
                        escribir_log(
                            alarmas_o_prevencion='prevencion', 
                            tipo_alarma='SCRIPT TMP', 
                            motivo='Se encontro un archivo de tipo script (#! primera linea), se movio a cuarentena', 
                            ip_o_email=new_diccionary['ruta_archivo']
                        )
            except Exception:
                print("El archivo esta codeado en bytes")
        
    for archivo in archivos_a_cuarentena:
        try:
            os.system(f"sudo mv {archivo['ruta_archivo']} {archivo['ruta_a_mover']}")
        except Exception:
            print(f"No se pudo mover a cuarentena el archivo: {archivo}.")
    


    #Procedemos a escribir en el archivo
    if archivos_a_cuarentena:    
        msg = "Ya se movio los ultimos archivos"
        func_enviar_mail(asunto="SE ENCONTRO SCRIPTS EN /tmp", mensaje=  listamsg)
    else:
        msg = "No se encontro archivos sospechosos en /tmp/"
        listamsg.append(HTML(msg))
   
    return listamsg
   
