from hipsbot.views.Herramientas.HTML import HTML


def ayuda():
    listamsg = []
    f1 = "1 : Verificar binarios"
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
    listamsg.append(HTML(f1))
    listamsg.append(HTML(f2))
    listamsg.append(HTML(f3))
    listamsg.append(HTML(f4))
    listamsg.append(HTML(f5))
    listamsg.append(HTML(f6))
    listamsg.append(HTML(f7))
    listamsg.append(HTML(f8))
    listamsg.append(HTML(f9))
    listamsg.append(HTML(f10))
    listamsg.append(HTML(f11))
    listamsg.append(HTML(f12))
    listamsg.append(HTML(f13))
    return listamsg
    