__author__ = 'jli3'
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from code_challenge.forms import *
import random

@transaction.atomic
@login_required
def random_pick(request):
    print "Here random pick"
    random_problem = Problem.objects.order_by('?').first()
    print random_problem
    if not random_problem:
        user = request.user
        problems = Problem.objects.all()
        return render(request, 'code_challenge/global_stream.html', {'problems': problems, 'currentuser': user})
    context = {'problem': random_problem, 'currentuser': request.user}
    return render(request, 'code_challenge/problem.html', context)
