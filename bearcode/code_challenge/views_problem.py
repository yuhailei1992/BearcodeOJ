__author__ = 'jiaxix'
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from code_challenge.forms import *

@transaction.atomic
def add_problem(request):
    print "add_problem"
    context = {}
    if request.method == 'GET':
        print "add_problem in GET, should not be here"
        context['form'] = ProblemForm()
        return render(request, 'code_challenge/add_problem.html', context)

    # if method is POST, get form data to update the model
    form = ProblemForm(request.POST, request.FILES)
    context['form'] = form

    if not form.is_valid():
        print "An invalid form!"
        return render(request, 'code_challenge/add_problem.html', context)

    form.save()
    return redirect(reverse('home'))