from django.core.mail import send_mail
from hips.settings import  EMAIL_HOST_USER
EMAIL_ADMIN     = 'fecabis954@meidir.com'
def func_enviar_mail(asunto,mensaje):
    print("falla")
    send_mail(asunto,mensaje,EMAIL_HOST_USER,[EMAIL_ADMIN])
    


