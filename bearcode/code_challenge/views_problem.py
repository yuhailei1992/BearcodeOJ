from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist

from views_submission import *


@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
@transaction.atomic
def add_problem(request):
    context = {}
    if request.method == 'GET':
        context['form'] = ProblemForm()
        return render(request, 'code_challenge/add_problem.html', context)

    # If method is POST, get form data to update the model.
    form = ProblemForm(request.POST, request.FILES)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'code_challenge/add_problem.html', context)

    form.save()
    problems = Problem.objects.all()
    context['problems'] = problems
    return render(request, 'code_challenge/manage_problem.html', context)


def permission_denied(request):
    return render(request, 'code_challenge/permission_denied.html', {})


@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
@transaction.atomic
def manage_problem(request):
    problems = Problem.objects.all()
    return render(request, 'code_challenge/manage_problem.html', {'problems': problems})


@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
@transaction.atomic
def edit_problem(request, problemid):
    context = {}
    problem_to_edit = get_object_or_404(Problem, id=problemid)
    context['problem'] = problem_to_edit

    # For GET requests, return the existing problem to edit.
    if request.method == 'GET':
        form = ProblemForm(instance=problem_to_edit)
        context['form'] = form
        return render(request, 'code_challenge/edit_problem.html', context)

    # For POST requests, add a new problem.
    form = ProblemForm(request.POST, request.FILES, instance=problem_to_edit)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'grumblr/edit_problem.html', context)

    form.save()

    # Load a new manage_problem page.
    problems = Problem.objects.all()
    context['problems'] = problems
    return render(request, 'code_challenge/manage_problem.html', context)


@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
@transaction.atomic
def delete_problem(request, problemid):
    # Deletes item if the logged-in user has an item matching the id.
    try:
        problem_to_delete = get_object_or_404(Problem, id=problemid)
        problem_to_delete.delete()
    except ObjectDoesNotExist:
        print 'Trying to delete a nonexistent problem.'

    context = {}
    problems = Problem.objects.all()
    context['problems'] = problems
    return render(request, 'code_challenge/manage_problem.html', context)


@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
@transaction.atomic
def enable_problem(request, problemid):
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
def disable_problem(request, problemid):
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
def test_problem(request, problemid):
    curr_problem = get_object_or_404(Problem, id=problemid)
    context = {'problem': curr_problem}
    return render(request, 'code_challenge/problem_internal_test.html', context)


@login_required
@permission_required('code_challenge.problem_mgmt', login_url="/permission_denied")
@transaction.atomic
def test_submit(request):
    submit_content = request.POST['codecontent']
    submit_lang = request.POST['language']
    problemid = request.POST['problemid']

    # Check submit_lang. The submit_lang must be in allowed_languages.
    if submit_lang not in allowed_languages:
        print 'Invalid language choice'
        return render(request, 'code_challenge/result.json', context_invalid_language,
                      content_type="application/json")

    # Analyze submitted code. If considered dangerous, the code will be rejected.
    if not submit_content or len(submit_content) == 0:
        print 'Null or void submitted content'
        return render(request, 'code_challenge/result.json', context_empty_content,
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
    curr_problem = get_object_or_404(Problem, id=problemid)

    # The parameters to be sent to docker.
    values = {'user_code': submit_content,
              'tle': curr_problem.tle_limit}
    if submit_lang == 'java':
        values['language'] = 'Java'
        values['test_code'] = curr_problem.java_tests
    else:
        values['language'] = 'Python'
        values['test_code'] = curr_problem.python_tests

    # Construct a request to the remote executor.
    data = urllib.urlencode(values)
    u = urllib.urlopen(worker_url % data)

    # Get the judge results and parse to a json object.
    u_str = str(u.read())
    judge_result = json.loads(u_str)

    return render(request, 'code_challenge/result.json', judge_result,
                  content_type="application/json")
