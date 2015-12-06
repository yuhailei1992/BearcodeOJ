__author__ = 'jiaxix'
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from code_challenge.forms import *
from django.contrib.auth.decorators import permission_required
import urllib
import json

allowed_languages = ['Python', 'Java']

@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
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

def permission_denied(request):
    print "Admin permission denied!"
    return render(request, 'code_challenge/permission_denied.html', {})

@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
@transaction.atomic
def manage_problem(request):
    problems = Problem.objects.all()
    print "There are " + str(len(problems)) + " problems in the list"
    return render(request, 'code_challenge/manage_problem.html',{'problems': problems})

@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
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

@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
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

@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
@transaction.atomic
def enable_problem(request,problemid):
    problem_to_enable = get_object_or_404(Problem, id=problemid)
    problem_to_enable.visible = True
    problem_to_enable.save()

    context = {}
    problems = Problem.objects.all()
    context['problems'] = problems
    return render(request, 'code_challenge/manage_problem.html', context)

@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
@transaction.atomic
def disable_problem(request,problemid):
    problem_to_enable = get_object_or_404(Problem, id=problemid)
    problem_to_enable.visible = False
    problem_to_enable.save()

    context = {}
    problems = Problem.objects.all()
    context['problems'] = problems
    return render(request, 'code_challenge/manage_problem.html', context)

@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
@transaction.atomic
def test_problem(request,problemid):
    curr_problem = Problem.objects.get(id=problemid)
    context = {'problem': curr_problem}
    return render(request, 'code_challenge/problem_internal_test.html', context)

@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
@transaction.atomic
def test_submit(request):
    print "in test_submit!!!!"
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
    if submit_lang == 'java':
        values['language'] = 'Java'
        values['test_code'] = curr_problem.java_tests
    else:
        values['language'] = 'Python'
        values['test_code'] = curr_problem.python_tests

    print values

    data = urllib.urlencode(values)
    u = urllib.urlopen("http://52.26.238.153/worker/judge/?%s" % data)
    print 'results from docker'
    u_str = str(u.read())
    print u_str

    context = json.loads(u_str)

    print context
    return render(request, 'code_challenge/result.json', context, content_type="application/json")