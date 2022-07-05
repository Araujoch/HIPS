from asyncio import subprocess
import datetime
import os
import subprocess
'''
    Mueve las herramientas Sniffer a una carpeta cuarentena
'''
def cuarentena(herramienta):
    
    cuarentena_sniffer = '/root/cuarentena/sniffer_tools'
  

    cmd = f"sudo find / -name {herramienta} -type f"
    rutas_encontradas = os.popen(cmd).read().split('\n')
    rutas_encontradas.pop(-1)
    print("rutas encontradas")
    print(rutas_encontradas)
    for path in rutas_encontradas:
            
            #Procedemos a mover el arhivo 
            new_file_name = path[1:].replace("/", "-")
            new_path = cuarentena_sniffer + new_file_name

            os.system(f"sudo mv -f {path} {new_path}")

            time_actual = datetime.datetime.now()
        

    if not len(rutas_encontradas):
        print(rutas_encontradas)
