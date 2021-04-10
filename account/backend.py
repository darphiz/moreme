from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate, login
from .models import Profile
import random
import string


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def anonymous_or_real(request):
    # do we have an existing user?
    if request.user.is_authenticated:
        return request.user
    else:
        # if not, create an anonymous user and log them in
        username = "Guest_"+get_random_string(6)
        u = User(username=username, first_name='Anonymous',
                 last_name='User')
        u.set_unusable_password()
        u.save()
        p = Profile(user=u, is_anonymous=True, image=None)
        p.save()
        authenticate(user=u)
        login(request, u)
        return u

######## Anonymous authentication backend middleware #########
