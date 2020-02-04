from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User


@api_view(['POST'])
def register(request):
    User.objects.create_user(request.POST.get('username', ''), request.POST.get('email', ''), request.POST.get('password', ''))
    return Response('Account successfully created', status=status.HTTP_200_OK)
