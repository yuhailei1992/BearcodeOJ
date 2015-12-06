import json
import urllib

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from code_challenge.forms import *
from code_challenge.models import *
from views import logger

# Allowed languages.
allowed_languages = ['Python', 'Java']
# The worker url.
worker_url = "http://52.26.238.153/worker/judge/?%s"
context_require_post = {'status': 'Internal Error', 'message': 'Please send POST requests.'}
context_invalid_language = {'status': 'Rejected', 'message': 'Invalid programming language choice'}
context_empty_content = {'status': 'Rejected', 'message': 'Null or void submitted content'}


@login_required
@transaction.atomic
def try_submit(request):
    logger.debug('>> try_submit')
    if request.method == 'GET':
        return render(request, 'code_challenge/result.json', context_require_post,
                      content_type="application/json")

    # Check request.POST.
    params = request.POST
    if params is None:
        return render(request, 'code_challenge/result.json', context_empty_content,
                      content_type="application/json")

    if 'codecontent' not in params or 'language' not in params or 'problemid' not in params:
        return render(request, 'code_challenge/result.json', context_empty_content,
                      content_type="application/json")

    # Get all the parameters from request.POST
    submit_content = params['codecontent']
    submit_lang = params['language']
    problemid = params['problemid']

    # Check for submit_lang. The submit_lang must be in allowed_languages.
    if submit_lang not in allowed_languages:
        return render(request, 'code_challenge/result.json', context_invalid_language,
                      content_type="application/json")

    # Analyze submitted code. If considered dangerous, the code will be rejected.
    if not submit_content or len(submit_content) == 0:
        return render(request, 'code_challenge/result.json', context_empty_content,
                      content_type="application/json")

    import views_code_analysis
    check_result = views_code_analysis.check_code(submit_content, submit_lang)

    if check_result['status'] == 'False':
        msg = format('The code should not contain such substring: %s' % check_result['message'])
        context = {'status': 'Rejected', 'message': msg}
        return render(request, 'code_challenge/result.json', context,
                      content_type="application/json")

    # After all the security checks, submit user code to oj_worker.
    context = {}
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

    # Prepare a request.
    data = urllib.urlencode(values)

    # Send request to oj_worker.
    u = urllib.urlopen(worker_url % data)
    u_str = str(u.read())

    judge_result = json.loads(u_str)

    # Save the submission result to user's submission history.
    new_history = SubmitHistory(text=submit_content, user=request.user, problem=curr_problem,
                                result=judge_result['status'])
    new_history_form = HistoryForm(request.POST, instance=new_history)
    if not new_history_form.is_valid():
        context['form'] = new_history_form
        new_history.save()

        profile_to_edit = get_object_or_404(UserProfile, user=request.user)
        submissions_prob = SubmitHistory.objects.filter(problem=curr_problem)
        if len(submissions_prob) != 0:
            accepted = 0
            for submission in submissions_prob:
                if 'Accept' in submission.result:
                    accepted += 1

            # Calculate acceptance rate.
            success_rate_prob = float(accepted) / len(submissions_prob) * 100
            success_rate_prob = round(success_rate_prob, 2)
            curr_problem.success_rate = str(success_rate_prob) + '%'
            curr_problem.save()

        submissions_user = SubmitHistory.objects.filter(problem=curr_problem)
        if len(submissions_user) != 0:
            accepted = 0
            for submission in submissions_user:
                if 'Accept' in submission.result:
                    accepted += 1

            success_rate_user = float(accepted) / len(submissions_user) * 100
            success_rate_user = round(success_rate_user, 2)
            # print success_rate_user
            profile_to_edit.success_rate = str(success_rate_user) + '%'
            profile_to_edit.save()

        return render(request, 'code_challenge/result.json', context,
                      content_type="application/json")

    context['form'] = new_history_form
    new_history.save()
    new_history_form.save()

    profile_to_edit = get_object_or_404(UserProfile, user=request.user)
    submissions_prob = SubmitHistory.objects.filter(problem=curr_problem)
    if len(submissions_prob) != 0:
        print 'IN TRY SUBMIT SUBMISSION PROBLEM'
        accepted = 0
        for submission in submissions_prob:
            if 'Accept' in submission.result:
                print 'IN TRY SUBMIT SUBMISSION PROBLEM ACCEPT' + str(accepted)
                accepted += 1
        success_rate_prob = accepted / len(submissions_prob)
        print success_rate_prob
        curr_problem.success_rate = success_rate_prob
        curr_problem.save()
    submissions_user = SubmitHistory.objects.filter(problem=curr_problem)
    if len(submissions_user) != 0:
        print 'IN TRY SUBMIT SUBMISSION USER'
        accepted = 0
        for submission in submissions_user:
            if 'Accept' in submission.result:
                print 'IN TRY SUBMIT SUBMISSION USER ACCEPT' + str(accepted)
                accepted += 1

        success_rate_user = accepted / len(submissions_user)
        print success_rate_user
        profile_to_edit.success_rate = success_rate_user
        profile_to_edit.save()

    print context
    return render(request, 'code_challenge/result.json', context, content_type="application/json")


@login_required
@transaction.atomic
def submit_history(request, problemid):
    curr_problem = get_object_or_404(Problem, id=problemid)
    histories = SubmitHistory.objects.filter(problem=curr_problem).order_by('-created_at')
    context = {'problem': curr_problem,
               'histories': histories}
    return render(request, 'code_challenge/submit_history.html', context)


@login_required
@transaction.atomic
def submit_details(request, historyid):
    history = get_object_or_404(SubmitHistory, id=historyid)
    curr_problem = history.problem
    context = {'history': history,
               'problem': curr_problem}
    return render(request, 'code_challenge/submit_details.html', context)
