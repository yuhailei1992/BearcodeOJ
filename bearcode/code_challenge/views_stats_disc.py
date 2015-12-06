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
    # print "Here random pick"
    random_problem = Problem.objects.order_by('?').first()
    # print random_problem
    if not random_problem:
        # user = request.user
        problems = Problem.objects.all()
        return render(request, 'code_challenge/global_stream.html', {'problems': problems, 'currentuser': request.user})
    context = {'problem': random_problem}
    return render(request, 'code_challenge/problem.html', context)

@transaction.atomic
@login_required
def search_discussion_page(request):
    discussions = Discussion.objects.all().order_by('-created_at')    
    # print 'Discussions' + str(discussions)
    return render(request, 'code_challenge/search_discussion.html', {'discussions': discussions, 'currentuser': request.user})

@transaction.atomic
@login_required
def search_discussion(request):
    # print "In Search Discussion"
    context = {}
    if request.method == 'POST':
        # print 'search method set to post'
        # show all the discussions
        #discussions = Discussion.objects.all().order_by('-created_at')
        return render(request, 'code_challenge/search_discussion.html', context)
    
    userInput = request.GET['userInput'].lower()
    # print userInput
    # get all the discussions and search for the input
    candidates = Discussion.objects.all().order_by('-created_at')    
    discussions = set()
    for discussion in candidates:
        # print discussion
        if userInput in discussion.title.lower() or userInput in discussion.text.lower():
            discussions.add(discussion)

    context['discussions'] = discussions
    print discussions
    return render(request, 'code_challenge/search_discussion.html', context)

@transaction.atomic
@login_required
def ranking_board(request):
    context = {}

    userprofiles = UserProfile.objects.filter(role="nuser").order_by('-success_rate')

    context['userprofiles'] = userprofiles

    return render(request, 'code_challenge/ranking_board.html', context)

