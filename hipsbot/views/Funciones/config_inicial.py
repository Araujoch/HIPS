import os
import subprocess
from hipsbot.models import CheckSuma, Sniffer
def initialconfig():
    '/root/cuarentena'
    
    if os.path.exists('/root/cuarentena') is False:
        subprocess.call(['mkdir','/root/cuarentena'])
    if os.path.exists('/root/cuarentena/sniffer_tools') is False:
        subprocess.call(['mkdir','/root/cuarentena/sniffer_tools'])
    if os.path.exists('/root/cuarentena/tmp_scripts') is False:
        subprocess.call(['mkdir','/root/cuarentena/tmp_scripts'])
    if os.path.exists('/var/log/hips/alarmas.log') is False:
        subprocess.call(['touch','/root/cuarentena/tmp_scripts'])
    if os.path.exists('/var/log/hips/prevencion.log') is False:
        subprocess.call(['touch','/root/cuarentena/tmp_scripts'])
    
   

    programas = []
    binarios  = ['/etc/passwd','/etc/shadow','/etc/group']
    for auxprograma in programas:
        s = Sniffer(programa = auxprograma)
        s.save()
    for archivo in binarios:
        h = subprocess.run(['sudo','md5sum',archivo],capture_output=True ).stdout.decode('utf-8')
        c = CheckSuma(directorio = archivo , hashsuma = h )
        c.save()
initialconfig()