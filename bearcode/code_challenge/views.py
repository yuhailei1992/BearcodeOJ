import logging

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from code_challenge.models import *

logger = logging.getLogger(__name__)

admin_username = "bearcode2015@gmail.com"


@login_required
def home(request):
    user = request.user

    # For administrators.
    if user.username == admin_username:
        return redirect(reverse('manageproblem'))

    problems = Problem.objects.all()

    return render(request, 'code_challenge/global_stream.html', {'problems': problems})


@login_required
@transaction.atomic
def problem(request, problemid):
    curr_problem = get_object_or_404(Problem, id=problemid)
    context = {'problem': curr_problem}
    return render(request, 'code_challenge/problem.html', context)


def welcome(request):
    return render(request, 'code_challenge/welcome.html', {})


def about(request):
    return render(request, 'code_challenge/about.html', {})
