import os
def bloquear_ip(ip):
    os.system(f"route add -host  {ip} reject")
    #os.system("sudo service iptables save")
