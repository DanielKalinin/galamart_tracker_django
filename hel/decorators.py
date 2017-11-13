from hel.models import User
from django.http import HttpResponseRedirect

#TODO: make wrappers accept optional arguments

def for_authorized(view):
    def wrapper(request):
        if not 'app_user_authorized' in request.sesstion \
           or not request.session['app_user_authorized']:
            return HttpResponseRedirect('/login/')

        return view(request)

    return wrapper

def for_appointed(view):
    def wrapper(request):
        user = User.objects.get(pk=request.session['app_user_id'])
        if not user.role:
            HttpResponseRedirect('/profile/appoint/')

        return view(request)
