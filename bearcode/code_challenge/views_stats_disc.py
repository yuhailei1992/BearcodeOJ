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
    """
    Randomly pick a problem for the current user to solve
    :param request: the request to pick random problem
    :return: a dict containing the status and the message
    """
    shuffle_problems = Problem.objects.filter(visible=True).order_by('?')
    if not shuffle_problems:
        problems = Problem.objects.all()
        return render(request, 'code_challenge/global_stream.html', {'problems': problems, 'currentuser': request.user})

    print "random pick, get "+str(len(shuffle_problems))+" problems here"
    context = {'problem': shuffle_problems[0]}
    return render(request, 'code_challenge/problem.html', context)

@transaction.atomic
@login_required
def search_discussion_page(request):
    """
    The discussions page where all the discussions displayed and user can search for specific discussion
    :param request: the request to display discussions available
    :return: a dict containing the status and the message
    """
    discussions = Discussion.objects.all().order_by('-created_at')    
    return render(request, 'code_challenge/search_discussion.html', {'discussions': discussions, 'currentuser': request.user})

@transaction.atomic
@login_required
def search_discussion(request):
    """
    The discussions page where specific discussions displayed with certain keyword
    :param request: the specific keyword to search
    :return: a dict containing the status and the message
    """
    context = {}
    if request.method == 'POST':
        # show all the discussions
        return render(request, 'code_challenge/search_discussion.html', context)
    
    userInput = request.GET['userInput'].lower()
    # get all the discussions and search for the input
    candidates = Discussion.objects.all().order_by('-created_at')    
    discussions = set()
    for discussion in candidates:
        if userInput in discussion.title.lower() or userInput in discussion.text.lower():
            discussions.add(discussion)

    context['discussions'] = discussions
    return render(request, 'code_challenge/search_discussion.html', context)

@transaction.atomic
@login_required
def ranking_board(request):
    """
    The ranking board page where all the users are ranked according to their success rate
    :param request: the request to rank the users
    :return: a dict containing the status and the message
    """
    context = {}

    userprofiles = UserProfile.objects.filter(role="nuser").order_by('-success_rate')

    context['userprofiles'] = userprofiles

    return render(request, 'code_challenge/ranking_board.html', context)

