from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from compositions.models import UserProfile, Composition
from django.contrib.auth.models import User
from compositions.forms import AddCompositionForm, GradeCompositionForm
from random import randint
from shutil import copyfile


from django.template import RequestContext
import os



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
        ungraded_compositions = Composition.objects.filter(grade=0)
        all_compositions = Composition.objects.filter()
        return render_to_response('compositions/grade.html', {'ungraded_compositions': ungraded_compositions, 'all_compositions': all_compositions}, context)
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
    #with open('files/simple.ly', "w"):
        #pass
    #os.remove('files/simple.ly')
    f = open('files/simple.ly', "w+")
    f.write ('\\version "2.16.2"\n')
    f.write("\\relative c' {\n")
    f.write(" ".join(order))
    f.write('\n}')
    f.close()
    
    os.system('files/script.sh')
    
    #python doesn't have a do while loop, so i emulate a do until - I need to do this just to make to sure that the random generated number we selected is unique
    while True:
        pdf_path = "files/pdf" + str(randint(100000000, 999999999))
        if not os.path.isfile(pdf_path):
            break

    copyfile('simple.pdf', pdf_path)
    os.remove('simple.pdf')
    new_comp = Composition(user=current_user, order=order, pdf_path=pdf_path)
    new_comp.save()
    return order

@login_required
def show_pdf(request, composition_id):
    current_user = request.user
    current_user_profile = UserProfile.objects.get(user_id=current_user.id)

    composition = Composition.objects.get(id=composition_id)

    pdf_path = composition.pdf_path

    if not current_user.is_superuser:
        if composition.user.id == current_user.id or current_user_profile.professor:
            image_data = open(pdf_path, 'rb').read()
            return HttpResponse(image_data, content_type='application/pdf')
        else:
            return HttpResponse('You don\'t have the necessary permission')
    else:
        image_data = open(path, 'rb').read()
        return HttpResponse(image_data, content_type='application/pdf')

@login_required
def grade_pdf(request, composition_id):
    current_user = request.user
    current_user_profile = UserProfile.objects.get(user_id=current_user.id)

    if current_user_profile.professor:
        context = RequestContext(request)
        if request.method == 'POST':
            form = GradeCompositionForm(request.POST, request.FILES)
            if form.is_valid():
                ret = change_comp(request, composition_id)

        else:
            form = GradeCompositionForm(
                initial={'grade': 0, 'comment': ''}
            )
        return render_to_response('compositions/grade_comp.html', {'form': form, 'composition_id': composition_id}, context)
    else:
        return HttpResponse('You don\'t have the necessary permission')

@login_required 
def change_comp(request, composition_id):
    composition = Composition.objects.get(id=composition_id)
    composition.grade = request.POST['grade']
    composition.comment = request.POST['comment']
    composition.save()
    return composition_id

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
        user_profile = UserProfile.objects.get(user_id=user.id)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.

                login(request, user)
                if user_profile.professor:
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