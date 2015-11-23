__author__ = 'jiaxix'
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
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
    problems = Problem.objects.all()
    context['problems'] = problems
    return render(request, 'code_challenge/manage_problem.html', context)

@transaction.atomic
def manage_problem(request):
    problems = Problem.objects.all()
    print "There are " + str(len(problems)) + " problems in the list"
    return render(request, 'code_challenge/manage_problem.html',{'problems': problems})


@transaction.atomic
def edit_problem(request, problemid):
    #return redirect(reverse('home'))
    context = {}
    problem_to_edit = get_object_or_404(Problem, id=problemid)
    context['problem'] = problem_to_edit

    if request.method == 'GET':
        form = ProblemForm(instance=problem_to_edit)
        context['form']=form
        return render(request, 'code_challenge/edit_problem.html', context)

    form = ProblemForm(request.POST, request.FILES, instance=problem_to_edit)

    if not form.is_valid():
        print "edit-problem: form not valid"
        context['form']=form
        return render(request, 'grumblr/edit_problem.html', context)

    print "valid update problem form, to save..."
    form.save()

    problems = Problem.objects.all()
    context['problems'] = problems
    return render(request, 'code_challenge/manage_problem.html', context)

@transaction.atomic
def delete_problem(request,problemid):
    errors = []

    # Deletes item if the logged-in user has an item matching the id
    try:
        problem_to_delete = Problem.objects.get(id=problemid)
        problem_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The post does not exist in the whole database')

    context = {}
    problems = Problem.objects.all()
    context['problems'] = problems
    return render(request, 'code_challenge/manage_problem.html', context)