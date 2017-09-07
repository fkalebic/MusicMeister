from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from compositions.models import UserProfile, Composition
from django.contrib.auth.models import User
from compositions.forms import AddCompositionForm

from django.template import RequestContext


@login_required
def welcome(request):
    #return HttpResponse("Hello, world. You're at the student index.")
    context = RequestContext(request)
    current_user_id = request.user.id
    all_compositions = Composition.objects.filter(user_id=current_user_id)
    return render_to_response('compositions/welcome.html', {'all_compositions': all_compositions}, context)

@login_required
def grade(request):
    context = RequestContext(request)
    current_user_profile = UserProfile.objects.get(user_id=request.user)
    if current_user_profile.professor:
        all_compositions = Composition.objects.filter(grade=0)
        return render_to_response('compositions/grade.html', {'all_compositions': all_compositions}, context)
    else:
        return HttpResponse("Nein! Verboten! Only professors can access this page!")

@login_required
def add_new_comp(request):
#    context = RequestContext(request)
#    current_user_id = request.user.id
#    all_compositions = Composition.objects.filter(user_id=current_user_id)
#    return render_to_response('compositions/welcome.html', {'all_compositions': all_compositions}, context)
    context = RequestContext(request)
    if request.method == 'POST':
        form = AddCompositionForm(request.POST, request.FILES)
        if form.is_valid():
            ret = save_comp(request)

    else:
        form = AddCompositionForm(
            initial={'order': ''}
        )
    return render_to_response('compositions/add_new_comp.html', {'form': form}, context)

@login_required
def save_comp(request):
    order = request.POST['order']
    current_user = request.user
    new_comp = Composition(user=current_user, order=order)
    new_comp.save()
    return order


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.

                login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect('/compositions/grade/')
                else:
                    return HttpResponseRedirect('/compositions/welcome/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('compositions/login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/compositions/')