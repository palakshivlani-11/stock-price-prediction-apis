from .views import *
from django.urls import path , include
from knox import views as knox_views


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    # path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('getdata/',GetData.as_view(), name='getdata'),
     
    
]