# import logging

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from code_challenge.models import *

# logger = logging.getLogger(__name__)

admin_username = "bearcode2015@gmail.com"


@login_required
def home(request):
    """
    the global stream for the whole site, including all the problems to solve
    :param request: the request to the global stream
    :return: a dict containing the status and message
    """
    user = request.user

    # For administrators.
    if user.username == admin_username:
        return redirect(reverse('manageproblem'))

    problems = Problem.objects.all()

    return render(request, 'code_challenge/global_stream.html', {'problems': problems})


@login_required
@transaction.atomic
def problem(request, problemid):
    """
    the problem page for the user to submit code
    :param request: user submitted request to display the specific problem
    :param problemid: the id of the problem to display
    :return: a dict containing the status and message
    """
    curr_problem = get_object_or_404(Problem, id=problemid)
    context = {'problem': curr_problem}
    return render(request, 'code_challenge/problem.html', context)


def welcome(request):
    """
    the welcome page before the user can login or sign up
    :param request: user request to the site
    :return: a dict containing the status and message
    """
    return render(request, 'code_challenge/welcome.html', {})


def about(request):
    """
    the about-us page for the contributors information
    :param request: user request to the site
    :return: a dict containing the status and message
    """
    return render(request, 'code_challenge/about.html', {})
