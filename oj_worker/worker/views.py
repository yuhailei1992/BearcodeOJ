from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from exec_java_file import run_java_code
from exec_py_file import run_py_code

@csrf_exempt
def judge(request):
    dict = request.GET
    print dict
    user_code = dict['user_code']
    test_code = dict['test_code']
    tle = int(dict['tle'])
    lang_type = dict['language']
    if lang_type == 'Java':
        context = run_java_code(test_code, user_code, tle)
    else:
        context = run_py_code(test_code, user_code, tle)
    return JsonResponse(context)

    # context = {'return_code': 1, 'return_msg': 'You have called the judge'}
    # return JsonResponse(context)
