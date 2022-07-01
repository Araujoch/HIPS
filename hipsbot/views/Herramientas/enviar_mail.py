from django.core.mail import send_mail
from hips.settings import  EMAIL_HOST_USER
EMAIL_ADMIN     = 'araujochi1609@gmail.com'
def func_enviar_mail(asunto,mensaje):

    send_mail(asunto,mensaje,EMAIL_HOST_USER,['pepitobro4@gmail.com',EMAIL_ADMIN])


