import re
#from django.contrib.auth.models import User


def validatepassword(password):
    if len(password) < 8:
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[~`^<>:;?*#@$!%&._+-=]", password):
        return False
    elif re.search("/s", password):
        return False
    return True


def validateusername(username):
    if len(username) > 20:
        return False
    for usr in username:
        if usr.isalnum():
            pass
        else:   
            return False
    else:
        return True