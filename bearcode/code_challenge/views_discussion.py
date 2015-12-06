from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from code_challenge.forms import *
from code_challenge.models import *

@login_required
@transaction.atomic
def add_comment(request, discussionid):
    curr_discussion = get_object_or_404(Discussion, id=discussionid)

    context = {'discussion': curr_discussion}
    if request.method == 'GET':
        print "come into get"
        context['form'] = CommentForm()
        return render(request, 'code_challenge/each_discussion.html', context)

    form = CommentForm(request.POST)
    if not form.is_valid():
        print "add comment: form is not valid"
        context['form'] = CommentForm()
        redirect(reverse('each_discussion', kwargs={'discussionid': discussionid}))

    print "add comment: valid form"
    new_comment = Comment(text=form.cleaned_data['commenttext'], user=request.user,
                          discussion=curr_discussion)
    new_comment.save()
    context['comments'] = Comment.objects.filter(discussion=curr_discussion).order_by(
        '-created_at')

    return redirect(reverse('each_discussion', kwargs={'discussionid': discussionid}))


@login_required
@transaction.atomic
def discussion(request, problemid):
    curr_problem = get_object_or_404(Problem, id=problemid)
    context = {'problem': curr_problem,
               'discussions': Discussion.objects.filter(problem=curr_problem)}
    return render(request, 'code_challenge/discussion.html', context)


@login_required
@transaction.atomic
def add_discussion(request, problemid):
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
    curr_discussion = get_object_or_404(Discussion, id=discussionid)
    context = {'discussion': Discussion.objects.get(id=discussionid),
               'comments': Comment.objects.filter(discussion=curr_discussion).order_by(
                   '-created_at')}

    return render(request, 'code_challenge/each_discussion.html', context)
