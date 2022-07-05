import os
import subprocess

from hipsbot.models import CheckSuma




def initialconfig():
    
    if os.path.exists('/root/cuarentena') is False:
        subprocess.call(['sudo','mkdir','/root/cuarentena'])
    if os.path.exists('/root/cuarentena/sniffer_tools') is False:
        subprocess.call(['sudo','mkdir','/root/cuarentena/sniffer_tools'])
    if os.path.exists('/root/cuarentena/tmp_scripts') is False:
        subprocess.call(['sudo','mkdir','/root/cuarentena/tmp_scripts'])
    if os.path.exists('/var/log/hips') is False:
        subprocess.call(['sudo','mkdir','/var/log/hips'])
    if os.path.exists('/var/log/hips/alarmas.log') is False:
        subprocess.call(['sudo','touch','/var/log/hips/alarmas.log'])
    if os.path.exists('/var/log/hips/prevencion.log') is False:
        subprocess.call(['sudo','touch','/var/log/hips/prevencion.log'])
    
   

    programas = []
    binarios  = ['/etc/passwd','/etc/shadow','/etc/group']
    for archivo in binarios:
        h = os.popen(f"md5sum {archivo}").read()
        c = CheckSuma(directorio = archivo , hashsuma = h )
        c.save()
