import os
def bloquear_ip(ip):
    os.system(f"sudo route -host {ip} reject")
    #os.system("sudo service iptables save")