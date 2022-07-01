import os
def  verificar_libreria(PID):
    cmd = f"sudo lsof -p {PID} -e /run/user/1000/gvfs | grep libpcap"
    print("LLEGUE")
    resultado_comando = os.popen(cmd).read().split('\n')
    resultado_comando.pop(-1)
    if not len(resultado_comando):
        return "NO"
    else:
        return "SI"