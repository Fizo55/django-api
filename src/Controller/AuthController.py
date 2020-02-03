# TODO : Get it via a POST Request
from django.contrib.auth.models import User
user = User.objects.create_user('test', 'test@test.test', 'test')