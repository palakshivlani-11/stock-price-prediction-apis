from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from django.contrib.auth import login
from .models import *
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated 
from . import serializers  
from .test import svm_model
import json
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

# Create your views here.
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        login_event = LoginEvent.objects.create(user=user)
        return super(LoginAPI, self).post(request, format=None)
    
class GetData(generics.GenericAPIView):
    permissions_classes = (permissions.IsAuthenticated)
    
    def post(self,request):
        curr = request.user
        serializer = GetDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stock_name = serializer.validated_data['stock_name']
        forecast_days = serializer.validated_data['forecast_days']
        stock_data = svm_model(forecast_days,stock_name)
        Useractivity.objects.create(user=curr,stock=stock_name,forecastdays=forecast_days,result=json.dumps(stock_data, cls=NumpyEncoder))
        if "error" in stock_data:
            return Response(stock_data,status=404)
        else:
            return Response(stock_data,status=200)
        
        
        
    
    
