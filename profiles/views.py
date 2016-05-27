from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from profiles.forms import UserCreationForm


def index(request):
    return render(request, 'profiles/index.html')


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your Django account is disabled.")
        else:
            print ("Invalid login details: %s, %s" % (username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('profiles/login.html', {}, context)


@login_required()
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')


# @csrf_exempt
def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.save()

            registered = True
        else:
            print(user_form.errors)

    else:
        user_form = UserCreationForm()

    return render_to_response('profiles/register.html',
                              {'user_form': user_form, 'registered': registered},
                              context
                              )
