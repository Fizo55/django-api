from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from validate_email import validate_email
import re
import requests
from django.conf import settings

@api_view(['POST'])
def register(request):
    email = request.POST.get('email', '')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    lname = request.POST.get('lname', '')
    captchaToken = request.POST.get('captchaToken', '')

    if not email or not username or not password or not lname:
        return Response('Please complete correctly the register form !', status=status.HTTP_400_BAD_REQUEST)

    if not validate_email(email):
        return Response('Please check if your email address is good', status=status.HTTP_400_BAD_REQUEST)

    if len(username) < 3:
        return Response('Your username need to have more than 3 letters', status=status.HTTP_400_BAD_REQUEST)

    if len(password) <= 8 and re.search('[0-9]', password) is None and re.search('[A-Z]', password) is None:
        return Response('Your password must contain at least one capital letter, one number and must be at least 8 characters long.', status=status.HTTP_400_BAD_REQUEST)

    r = requests.post(settings.GR_CAPTCHA_URL, {
        'secret': settings.GR_CAPTCHA_SECRET_KEY,
        'response': captchaToken
    })

    if not r.json()['success']:
        return Response('Please complete correctly the captcha !', status=status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(email=email)
        return Response('This email is already used', status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        try:
            User.objects.get(username=username)
            return Response('This username is already used', status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password)
            user.first_name = username
            user.last_name = lname
            user.save()
            return Response('Account successfully created', status=status.HTTP_200_OK)
