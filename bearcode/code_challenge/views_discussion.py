from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from code_challenge.forms import *
from code_challenge.models import *

@login_required
@transaction.atomic
def add_comment(request, discussionid):
    """
    Add comment to specific discussion under a problem
    :param request: the content of the comment
    :param discussionid: the id of the discussion to add comment
    :return: a dict containing the status and the message
    """
    curr_discussion = get_object_or_404(Discussion, id=discussionid)

    context = {'discussion': curr_discussion}
    if request.method == 'GET':
        context['form'] = CommentForm()
        return render(request, 'code_challenge/each_discussion.html', context)

    form = CommentForm(request.POST)
    if not form.is_valid():
        context['form'] = CommentForm()
        redirect(reverse('each_discussion', kwargs={'discussionid': discussionid}))

    new_comment = Comment(text=form.cleaned_data['commenttext'], user=request.user,
                          discussion=curr_discussion)
    new_comment.save()
    context['comments'] = Comment.objects.filter(discussion=curr_discussion).order_by(
        '-created_at')

    return redirect(reverse('each_discussion', kwargs={'discussionid': discussionid}))


@login_required
@transaction.atomic
def discussion(request, problemid):
    """
    Display discussions under a problem
    :param request: the request to display the discussions
    :param problemid: the id of the problem to display corresponding discussions
    :return: a dict containing the status and the message
    """
    curr_problem = get_object_or_404(Problem, id=problemid)
    context = {'problem': curr_problem,
               'discussions': Discussion.objects.filter(problem=curr_problem)}
    return render(request, 'code_challenge/discussion.html', context)


@login_required
@transaction.atomic
def add_discussion(request, problemid):
    """
    Add discussion to specific problem
    :param request: the content of the newly added discussion
    :param problemid: the id of the problem to add discussion
    :return: a dict containing the status and the message
    """
    curr_problem = get_object_or_404(Problem, id=problemid)
    context = {'problem': curr_problem,
               'discussions': Discussion.objects.filter(problem=curr_problem).order_by(
                   '-created_at')}
    if request.method == 'GET':
        return render(request, 'code_challenge/discussion.html', {'form': DiscussionForm()})

    form = DiscussionForm(request.POST)
    if not form.is_valid():
        print "add discussion: form not valid"
        context['form'] = form
        return render(request, 'code_challenge/discussion.html', context)

    print "add discussion: valid form!"

    new_discussion = Discussion(title=form.cleaned_data['discussiontitle'],
                                text=form.cleaned_data['discussiontext'], user=request.user,
                                problem=curr_problem)
    new_discussion.save()
    context['form'] = form
    return redirect(reverse('discussion', kwargs={'problemid': problemid}))


@login_required
@transaction.atomic
def each_discussion(request, discussionid):
    """
    The specific discussion with its comments
    :param request: the content of the discussion of its corresponding comments
    :param discussionid: the id of the discussion to display
    :return: a dict containing the status and the message
    """
    curr_discussion = get_object_or_404(Discussion, id=discussionid)
    context = {'discussion': Discussion.objects.get(id=discussionid),
               'comments': Comment.objects.filter(discussion=curr_discussion).order_by(
                   '-created_at')}

    return render(request, 'code_challenge/each_discussion.html', context)
