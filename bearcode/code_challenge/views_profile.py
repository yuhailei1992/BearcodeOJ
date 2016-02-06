import os
import time

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from code_challenge.forms import *
from code_challenge.models import *
from views import admin_username


def handle_uploaded_file(f):
    """
    Upload file to server
    :param request: the file to upload
    :return: a url of the uploaded file
    """
    if f:
        file_name, file_extension = os.path.splitext(f.name)
        url = '/static/photos/{}{}'.format(time.time(), file_extension)
        with open('./code_challenge' + url, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return url


@login_required
@transaction.atomic
def edit_profile(request):
    """
    Edit profile by the user if requested
    :param request: the request to edit the profile information
    :return: a dict containing the status and the message
    """
    profile_to_edit = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'GET':
        form = ProfileForm(instance=profile_to_edit)  # Creates form
        context = {'form': form}
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
                  {'form': form, 'userprofile': userprofile, 'posts': posts})


@login_required
@transaction.atomic
def profile(request, username):
    """
    display the corresponding profile as request
    :param request: the request to display the profile
    :param username: the username of the profile to be displayed
    :return: a dict containing the status and the message
    """
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)

    candidates = SubmitHistory.objects.filter(user=user).order_by('-created_at')
    problems = set()
    for submission in candidates:
        if submission.problem not in problems:
            problems.add(submission.problem)

    context = {'user': user, 'problems': problems, 'userprofile': user_profile}
    return render(request, 'code_challenge/profile.html', context)


@transaction.atomic
def register(request):
    """
    Register the user through the user auth
    :param request: the content of the registration information
    :return: a dict containing the status and the message
    """
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
    print "User role is " + new_profile.role
    if username == admin_username:
        print "Create Admin User"
        content_type = ContentType.objects.get_for_model(Problem)
        admin_permission = Permission.objects.create(codename="problem_mgmt",
                                                     name="Can manage problems",
                                                     content_type=content_type)
        new_user.user_permissions.add(admin_permission)
        new_profile.role = "admin"
        new_profile.save()
        if new_user.has_perm("code_challenge.problem_mgmt"):
            print "Successfully grant admin permission to user " + username
            print "Now User role is " + new_profile.role
        else:
            print "Grant Failure"

    login(request, new_user)
    return redirect(reverse('home'))
