# This file checks user-submitted code for security reasons.
import re

# forbid all the os, io, import functionalities.
python_keywords = ['import', 'sys', 'os', 'open', 'close', 'write', 'process', 'print', 'file', 'exec',
                   'reload', 'compile']

# java. is for preventing using external module without importing: java.util.List for example.
java_keywords = ['System', 'import', 'java.', 'org.', 'com.', '.io.', '.net.']

pass_ret_msg = {'status': 'True', 'message': 'Good job'}


def check_python_code(user_code):
    """ check for dangerous python keywords
    :param user_code: user submitted python code as a string
    :return: a dict containing the status and message
    """
    for keyword in python_keywords:
        re_pattern = re.compile(keyword)
        if bool(re_pattern.search(user_code)):
            return {'status': 'False', 'message': keyword}

    return pass_ret_msg


def check_java_code(user_code):
    """ check for dangerous java keywords
    :param user_code: user submitted java code as a string
    :return: a dict containing the status and message
    """
    for keyword in java_keywords:
        re_pattern = re.compile(keyword)
        if bool(re_pattern.search(user_code)):
            return {'status': 'False', 'message': keyword}

    return pass_ret_msg


def check_code(user_code, language):
    if language == 'python':
        return check_python_code(user_code)
    else:
        return check_java_code(user_code)
