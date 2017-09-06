from django.shortcuts import render

# Create your views here
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

import os


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")