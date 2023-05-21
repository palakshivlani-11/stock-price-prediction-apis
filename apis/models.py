from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
# Create your models here.

class LoginEvent(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_and_time = models.DateField(auto_now_add=True)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="stock price prediction"),
        # message:
        email_plaintext_message,
        # from:
        "shivlanipalak@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
    
class Useractivity(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_and_time = models.DateField(auto_now_add=True)
    stock = models.CharField(max_length=100)
    forecastdays = models.IntegerField()
    result = models.JSONField()