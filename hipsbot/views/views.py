
# Create your views here.
import subprocess
from django.http import HttpResponse
from hipsbot.models import CheckSuma, Sniffer
from hipsbot.views.Funciones.access_log import check_access_log
from hipsbot.views.Funciones.ataqueSMTP import check_ataques_smtp_messages
from hipsbot.views.Funciones.autenticacion_fallida import check_autenticacion_fallida
from hipsbot.views.Funciones.masivoscorreos import check_masivos_mail
from hipsbot.views.Funciones.md5sum import check_md5sum
from hipsbot.views.Funciones.sniffer import check_sniffer
from hipsbot.views.Funciones.usuarios_conectados import usuarios_conectados
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
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
    comandos = {"1":check_md5sum,
                "2":check_sniffer,
                "3":usuarios_conectados,
                "4":check_access_log ,
                "5":check_autenticacion_fallida,
                "6":check_ataques_smtp_messages,
                "7":check_masivos_mail}
    
    
    if entrada in comandos:
        return comandos[entrada]()
    else:
        msg = "Lo siento, no comprendo"
        return msg
def get_bot_response(request):

    entrada = request.GET['msg']
    
    return HttpResponse(BotRespuesta(entrada))

