from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from code_challenge.forms import *
from code_challenge.models import *


# @login_required
# @transaction.atomic
# def get_comments(request):
#     comments_set = Comment.get_comments(int(request.GET['post_id']))
#     comments = []
#     comments_iter = comments_set.iterator()
#     # Peek at the first item in the iterator.
#     try:
#         first_item = next(comments_iter)
#     except StopIteration:
#         # No rows were found, so do nothing.
#         context = {'size': 0, 'items': None}
#         return render(request, 'code_challenge/comments.json', context,
#                       content_type='application/json')
#     else:
#         # At least one row was found, so iterate over
#         # all the rows, including the first one.
#         from itertools import chain

#         for comment in chain([first_item], comments_iter):
#             profile_img = UserProfile.get_profile(comment.user.user.id).image

#             item = {'comment_user': comment.user.username, 'user_photo': profile_img,
#                     'created_at': comment.created_at, 'comment_text': comment.text}
#             print item
#             comments.append(item)

#     context = {'size': len(comments), 'comments': comments}
#     return render(request, 'code_challenge/comments.json', context, content_type='application/json')


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
