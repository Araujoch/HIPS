import os
import sys

from hipsbot.views.Herramientas.HTML import HTML
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail
from hipsbot.views.Herramientas.escribiri_log import escribir_log
from hipsbot.views.Herramientas.matar_proceso import kill_proceso
def get_proceso_por_mem_o_cpu(mem_o_cpu=""):
    print(mem_o_cpu)
    if mem_o_cpu == "mem" or mem_o_cpu == "cpu":
        PROCESOS_CON_MAS_CPU_O_MEM_CMD = f"ps -eo pid,%mem,%cpu --sort=-%{mem_o_cpu} | head -n 20 " # Devuelve los 20 procesos que mas cpu o memoria esta en uso.
        procesos_mas_memoria = os.popen(PROCESOS_CON_MAS_CPU_O_MEM_CMD).read().split("\n")
        procesos_mas_memoria.pop(-1)
        procesos_mas_memoria.pop(0)
        
        for index, proceso in enumerate(procesos_mas_memoria):
            tmp = proceso.split()

            nuevo_objeto = {
                "PID": int(tmp[0]),
                "%MEM": float(tmp[1]),
                "%CPU": float(tmp[2])
            }
            
            ver_tiempo_ejecutando_cmd = f"ps -p {nuevo_objeto['PID']} -o etime" # Comando para tener el tiempo de ejecucion del proceso en HH:MM:SS
            
            # Obtenemos el tiempo de ejecucion del proceso
            tiempo_ejecutandose = os.popen(ver_tiempo_ejecutando_cmd).read().split("\n")[1].strip().split(":") # Damos formato al retorno

            if len(tiempo_ejecutandose) < 3: # si no tiene hora, solo minutos y segundos
                tiempo_ejecutandose = float(tiempo_ejecutandose[0]) + float(tiempo_ejecutandose[1])/60.0 
            else:
                tiempo_ejecutandose = float(tiempo_ejecutandose[0]) * 60 + float(tiempo_ejecutandose[1]) + float(tiempo_ejecutandose[2])/60.0 
            
            nuevo_objeto["EXECUTION_TIME"] = round(tiempo_ejecutandose,2 ) # agregamos al objeto el tiempo de ejecucion
            procesos_mas_memoria[index] = nuevo_objeto

        return procesos_mas_memoria
    else:
        print("ERROR: el argumento debe ser 'mem' para memoria o 'cpu' para uso del procesador.")
        mensaje = {
            "mensaje": "error"
        }


# Se verifica que los recursos (CPU, RAM) no esten siendo abusados por parte de algun proceso
# En el caso de que se encuentre un proceso que abusa, se mata, se registra en logs de prevencion y se avisa al administrador por mail
def verificar_procesos_cpu_ram():
    listamsg = []
    men = 'mem'
    cpu = 'cpu'
    procesos_mas_memoria = get_proceso_por_mem_o_cpu(men)
    print(procesos_mas_memoria)
    procesos_mas_cpu = get_proceso_por_mem_o_cpu(cpu)
   # print(procesos_mas_cpu)
    procesos_a_matar = []
    cuerpo_email = ''

    # Revisamos el uso de las memorias
    for proceso in procesos_mas_memoria:
        #Si el consumo de ram supera el 80%
        if proceso["%MEM"] > 70.0:
      
            # Si el tiempo de uso de ram supera mas de 3 minutos
            if proceso["EXECUTION_TIME"] > 3.0:
                msg = f"El proceso: {proceso['PID']} uso mucho recursos de CPU en bastante tiempo, se procedio a matarlo"
                listamsg.append(HTML(msg))
                escribir_log(alarmas_o_prevencion='prevencion',
                tipo_alarma='MUCHA_RAM',
                ip_o_email=proceso['PID'],
                motivo='el proceso uso mucho recursos de memoria en bastante tiempo, se procedio a matarlo')
                proceso["motivo"] = "usa mucha memoria"
                procesos_a_matar.append(proceso)       
    # Revisamos el uso de los cpu
    for proceso in procesos_mas_cpu:
        
        #Si el consumo de CPU supera el 80%
        if proceso["%CPU"] > 70.0:
         

            if proceso["EXECUTION_TIME"] > 3.0:
                msg = f"El proceso: {proceso['PID']} uso mucho recursos de CPU en bastante tiempo, se procedio a matarlo"
                listamsg.append(HTML(msg)) 
                escribir_log(alarmas_o_prevencion='prevencion',
                             tipo_alarma='MUCHA_CPU', ip_o_email=proceso['PID'],
                             motivo='el proceso uso mucho recursos de CPU en bastante tiempo, se procedio a matarlo'
                            )
                proceso["motivo"] = "usa mucha cpu"
                procesos_a_matar.append(proceso)

    #Procedemos a matar los procesos que abusaron de los recursos
    for proceso in procesos_a_matar:
        kill_proceso(proceso['PID'])
        

    #Escribimos el archivo 
    msg = "No hubo consumo de recursos excesivos"
    listamsg.append(HTML(msg))
    if procesos_a_matar:
        msg = "Procesos matados.."
        func_enviar_mail(tipo_alerta='Prevencion!', asunto="MUCHO USO DE RECURSOS", cuerpo= listamsg)
        listamsg.append(HTML(msg))
        func_enviar_mail(tipo_alerta='Prevencion!', asunto="MUCHO USO DE RECURSOS", cuerpo= listamsg)
    
    return listamsg
