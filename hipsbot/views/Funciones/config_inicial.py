import os
import subprocess
from hipsbot.models import CheckSuma, Sniffer
def initialconfig():
    cuarentena = '/root/cuarentena'
    if os.path.exists(cuarentena) is False:
        subprocess.call(['mkdir',cuarentena])
   

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