from django.urls import path
from  hipsbot.views import views
urlpatterns = [
    path('',views.signin,name="login"),
    path('home',views.get_bot_response,name="home"),
   # path('get',views.get_bot_response,name="home/get")
    
  
]