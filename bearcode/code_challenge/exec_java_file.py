__author__ = 'cissy'

def run_code(test_code, user_code, timeout):
    context = {"status":"success", "message":""}
    context1 = {"status":"compile error", "message":"Cannot compile because ..."}

    return context