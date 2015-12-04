import os
import time
import urllib
import json
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from code_challenge.forms import *

# Allowed languages.
allowed_languages = ['Python', 'Java']
# The worker url.
worker_url = "http://52.26.238.153/worker/judge/?%s"


@login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    user = request.user
    problems = Problem.objects.all()
    print "There are " + str(len(problems)) + " problems in the list"
    return render(request, 'code_challenge/global_stream.html',
                  {'problems': problems, 'currentuser': user})


@login_required
@transaction.atomic
def discussion(request, problemid):
    curr_problem = Problem.objects.get(id=problemid)
    context = {'currentuser': request.user,
               'problem': curr_problem,
               'discussions': Discussion.objects.filter(problem=curr_problem)}
    return render(request, 'code_challenge/discussion.html', context)


@login_required
@transaction.atomic
def add_discussion(request, problemid):
    curr_problem = Problem.objects.get(id=problemid)
    context = {'currentuser': request.user,
               'problem': curr_problem}

    if request.method == 'GET':
        print "come into get"
        context['form'] = DiscussionForm()
        return render(request, 'code_challenge/discussion.html', context)

    new_discussion = Discussion(title=request.POST['discussiontitle'],
                                text=request.POST['discussiontext'], user=request.user,
                                problem=curr_problem)
    new_discussion_form = DiscussionForm(request.POST, instance=new_discussion)
    if not new_discussion_form.is_valid():
        context['form'] = new_discussion_form
        context['discussions'] = Discussion.objects.filter(problem=curr_problem).order_by(
            '-created_at')
        new_discussion.save()
        return redirect(reverse('discussion', kwargs={'problemid': problemid}))

    context['form'] = new_discussion_form
    context['discussions'] = Discussion.objects.filter(problem=curr_problem).order_by('-created_at')
    new_discussion.save()
    new_discussion_form.save()
    return redirect(reverse('discussion', kwargs={'problemid': problemid}))


@login_required
@transaction.atomic
def each_discussion(request, discussionid):
    curr_discussion = Discussion.objects.get(id=discussionid)
    context = {'currentuser': request.user,
               'discussion': Discussion.objects.get(id=discussionid),
               'comments': Comment.objects.filter(discussion=curr_discussion).order_by(
                   '-created_at')}

    return render(request, 'code_challenge/each_discussion.html', context)


@login_required
@transaction.atomic
def add_comment(request, discussionid):
    curr_discussion = Discussion.objects.get(id=discussionid)

    context = {'currentuser': request.user,
               'discussion': curr_discussion}
    if request.method == 'GET':
        print "come into get"
        context['form'] = CommentForm()
        return render(request, 'code_challenge/each_discussion.html', context)

    new_comment = Comment(text=request.POST['commenttext'], user=request.user,
                          discussion=curr_discussion)
    new_comment_form = CommentForm(request.POST, instance=new_comment)
    if not new_comment_form.is_valid():
        context['form'] = new_comment_form
        context['comments'] = Comment.objects.filter(discussion=curr_discussion).order_by(
            '-created_at')
        new_comment.save()
        return redirect(reverse('each_discussion', kwargs={'discussionid': discussionid}))

    context['form'] = new_comment_form
    context['comments'] = Comment.objects.filter(discussion=curr_discussion).order_by('-created_at')
    new_comment.save()
    new_comment_form.save()
    return redirect(reverse('each_discussion', kwargs={'discussionid': discussionid}))


@login_required
@transaction.atomic
def add_post(request):
    if request.method == 'GET':
        context = {'form': PostForm()}
        return render(request, 'code_challenge/global_stream.html', context)

    return redirect(reverse('home'))


@login_required
@transaction.atomic
def get_comments(request):
    comments_set = Comment.get_comments(int(request.GET['post_id']))
    comments = []
    comments_iter = comments_set.iterator()
    # Peek at the first item in the iterator.
    try:
        first_item = next(comments_iter)
    except StopIteration:
        # No rows were found, so do nothing.
        context = {'size': 0, 'items': None}
        return render(request, 'code_challenge/comments.json', context,
                      content_type='application/json')
    else:
        # At least one row was found, so iterate over
        # all the rows, including the first one.
        from itertools import chain

        for comment in chain([first_item], comments_iter):
            profile_img = UserProfile.get_profile(comment.user.user.id).image

            item = {'comment_user': comment.user.username, 'user_photo': profile_img,
                    'created_at': comment.created_at, 'comment_text': comment.text}
            print item
            comments.append(item)

    context = {'size': len(comments), 'comments': comments}
    return render(request, 'code_challenge/comments.json', context, content_type='application/json')


@login_required
@transaction.atomic
def profile(request, username):
    user = get_object_or_404(User, username=username)
    userprofile = get_object_or_404(UserProfile, user=user)
    currentuser = request.user

    candidates = SubmitHistory.objects.filter(user=user).order_by('-created_at')
    problems = set()
    for submission in candidates:
        if submission.problem not in problems:
            problems.add(submission.problem)

    currentuserprofile = get_object_or_404(UserProfile, user=currentuser)

    context = {'user': user, 'problems': problems, 'userprofile': userprofile, 'currentuser': currentuser}
    return render(request, 'code_challenge/profile.html', context)


@login_required
@transaction.atomic
def follower_stream(request):
    user = request.user
    userprofile = get_object_or_404(UserProfile, user=user)
    following = userprofile.following.all()
    posts = Post.objects.filter(user__in=following).order_by('-created_at')

    context = {'userprofile': userprofile, 'posts': posts, 'currentuser': user}
    print len(posts)
    return render(request, 'code_challenge/follower_stream.html', context)


@login_required
@transaction.atomic
def edit_profile(request):
    profile_to_edit = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'GET':
        form = ProfileForm(instance=profile_to_edit)  # Creates form
        context = {'form': form, 'currentuser': request.user}
        print "We are here at GET in edit_profile"
        return render(request, 'code_challenge/edit_profile.html', context)

    # if method is POST, get form data to update the model
    form = ProfileForm(request.POST, instance=profile_to_edit)
    userprofile = None
    if form.is_valid():
        print "This is valid"
        print request.FILES.get('image', False)
        form.image = handle_uploaded_file(request.FILES.get('image', False))
        form.save()
        userprofile = get_object_or_404(UserProfile, user=request.user)
        userprofile.image = form.image
        userprofile.save()
    posts = Post.objects.filter(user=request.user).order_by('created_at').reverse()

    return render(request, 'code_challenge/profile.html',
                  {'form': form, 'userprofile': userprofile, 'currentuser': request.user,
                   'posts': posts})


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


@login_required
@transaction.atomic
def problem(request, problemid):
    curr_problem = Problem.objects.get(id=problemid)
    context = {'problem': curr_problem, 'currentuser': request.user}
    return render(request, 'code_challenge/problem.html', context)


@login_required
@transaction.atomic
def try_submit(request):
    print "in try_submit!!!!"
    submit_content = request.POST['codecontent']
    print 'submitted content is: ' + submit_content
    submit_lang = request.POST['language']
    print "selected language is: " + submit_lang

    # Check for submit_lang. The submit_lang must be in allowed_languages.
    if submit_lang not in allowed_languages:
        print 'Invalid language choice'
        context = {'status': 'Rejected', 'message': 'Invalid programming language choice'}
        return render(request, 'code_challenge/result.json', context,
                      content_type="application/json")

    # Analyze submitted code. If considered dangerous, the code will be rejected.
    if not submit_content or len(submit_content) == 0:
        print 'Null or void submitted content'
        context = {'status': 'Rejected', 'message': 'Null or void submitted content'}
        return render(request, 'code_challenge/result.json', context,
                      content_type="application/json")

    import views_code_analysis
    check_result = views_code_analysis.check_code(submit_content, submit_lang)
    print check_result
    if check_result['status'] == 'False':
        msg = format('The code should not contain such substring: %s' % check_result['message'])
        context = {'status': 'Rejected', 'message': msg}
        return render(request, 'code_challenge/result.json', context,
                      content_type="application/json")

    # After all the security checks, submit user code to oj_worker.
    problemid = request.POST['problemid']
    curr_problem = Problem.objects.get(id=problemid)

    # The parameters to be sent to docker.
    values = {'user_code': submit_content,
              'tle': curr_problem.tle_limit}
    if submit_lang == 'Java':
        values['language'] = 'Java'
        values['test_code'] = curr_problem.java_tests
    else:
        values['language'] = 'Python'
        values['test_code'] = curr_problem.python_tests

    print values

    data = urllib.urlencode(values)
    u = urllib.urlopen(worker_url % data)
    print 'results from docker'
    u_str = str(u.read())
    print u_str

    context = json.loads(u_str)
    print context
    # save to history
    new_history = SubmitHistory(text=submit_content, user=request.user, problem=curr_problem,
                                result=context['status'])
    new_history_form = HistoryForm(request.POST, instance=new_history)
    if not new_history_form.is_valid():
        context['form'] = new_history_form
        new_history.save()
        return render(request, 'code_challenge/result.json', context,
                      content_type="application/json")

    context['form'] = new_history_form
    new_history.save()
    new_history_form.save()
    print "history saved" + str(new_history)

    print context
    return render(request, 'code_challenge/result.json', context, content_type="application/json")


@login_required
@transaction.atomic
def submit_history(request, problemid):
    curr_problem = get_object_or_404(Problem, id=problemid)
    histories = SubmitHistory.objects.filter(problem=curr_problem).order_by('-created_at')
    context = {'currentuser': request.user,
               'problem': curr_problem,
               'histories': histories}
    return render(request, 'code_challenge/submit_history.html', context)


@login_required
@transaction.atomic
def submit_details(request, historyid):
    history = get_object_or_404(SubmitHistory, id=historyid)
    curr_problem = history.problem
    context = {'currentuser': request.user,
               'history': history,
               'problem': curr_problem}
    return render(request, 'code_challenge/submit_details.html', context)


def handle_uploaded_file(f):
    if f:
        file_name, file_extension = os.path.splitext(f.name)
        url = '/static/photos/{}{}'.format(time.time(), file_extension)
        with open('./code_challenge' + url, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return url


@login_required
@transaction.atomic
def change_password(request):
    return render(request, 'code_challenge/password_change_form.html',
                  {'currentuser': request.user})


@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'code_challenge/register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'code_challenge/register.html', context)

    username = form.cleaned_data['username']
    password = form.cleaned_data['password1']
    firstname = form.cleaned_data['firstname']
    lastname = form.cleaned_data['lastname']

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=username,
                                        password=password,
                                        first_name=firstname,
                                        last_name=lastname,
                                        email=username)
    new_user.save()

    # Logs in the new user and redirects to global stream
    new_user = authenticate(username=username,
                            password=password)

    # print new_user.username + 'before create profile'
    new_profile = UserProfile(user=new_user, username=username,
                              first_name=firstname,
                              last_name=lastname)
    new_profile.save()

    login(request, new_user)
    return redirect(reverse('home'))
