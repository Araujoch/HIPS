
# Create your views here.
import subprocess
from django.http import HttpResponse
from hipsbot.models import CheckSuma, Sniffer
from hipsbot.views.Funciones.access_log import check_access_log
from hipsbot.views.Funciones.ataqueDDOS import ataque_ddos_dns
from hipsbot.views.Funciones.ataqueSMTP import check_ataques_smtp_messages
from hipsbot.views.Funciones.autenticacion_fallida import check_autenticacion_fallida
from hipsbot.views.Funciones.colacorreo import check_cola_correo
from hipsbot.views.Funciones.help import ayuda
from hipsbot.views.Funciones.masivoscorreos import check_masivos_mail
from hipsbot.views.Funciones.md5sum import check_md5sum
from hipsbot.views.Funciones.procesos_muchos_recursos import get_proceso_por_mem_o_cpu
from hipsbot.views.Funciones.sniffer import check_sniffer
from hipsbot.views.Funciones.temp import verificar_script
from hipsbot.views.Funciones.usuarios_conectados import usuarios_conectados
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from hipsbot.views.Funciones.verificar_cron import verificar_cronjobs
from hipsbot.views.Herramientas.enviar_mail import func_enviar_mail

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password    = request.POST['password']
        print(username,password)
        user     = authenticate(username=username , password=password)
        if user is not None:
            login(request,user)
            return render(request,"index.html")
        
    return render(request, "login.html")
def home(request):
    print("HOLA")
    return redirect('index.html')

'''
    Retorna un HTMl con el salida de la operacion que eligio el usuario
'''
def BotRespuesta(entrada):
    '''Diccionario de Funciones sin parametro'''
    "1 : Verificar binarios"
    f2 = "2 : Herramientas Sniffer"
    f3 = "3 : Usuarios Conectados"
    f4 = "4 : Verificar archivo access.log"
    f5 = "5 : Verificar archivo secure"
    f6 = "6 : Verificar archivo messages"
    f7 = "7 : Verificar archivo maillog"
    f8 = "8 : Cpu y Memoria"
    f9 = "9 : Verificar temp"
    f10 = "10 : Cola correo"
    f11 = "11 : Verificar cron"
    f12 = "12 : Verificar tcpdump_dns(ataques DDOS)"
    f13 = "help : help"
    comandos = {"1":check_md5sum,
                "2":check_sniffer,
                "3":usuarios_conectados,
                "4":check_access_log ,
                "5":check_autenticacion_fallida,
                "6":check_ataques_smtp_messages,
                "7":check_masivos_mail,
                "8":get_proceso_por_mem_o_cpu,
                "9":verificar_script,
                "10":check_cola_correo,
                "11":verificar_cronjobs,
                "12":ataque_ddos_dns,
                "help":ayuda}
    
    
    if entrada in comandos:
        return comandos[entrada]()
    else:
        msg = "Lo siento, no comprendo"
        return msg
def get_bot_response(request):

    entrada = request.GET['msg']
    
    return HttpResponse(BotRespuesta(entrada))

