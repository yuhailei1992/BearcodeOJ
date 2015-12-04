import subprocess
from subprocess import CalledProcessError
import random
import os
import time

COMPILE = 'javac %s 2> %s'
# Need to cd to the working directory, then call java to execute the .class file.
RUN = 'cd %s && exec java %s 2> %s'
RAND_RANGE = 100000000
CLEAN = 'rm -r %s'
COMP_ERR_ANCHOR = 'Solution.java:'
COMP_ERR_ANCHOR_LEN = len(COMP_ERR_ANCHOR)


def find_nth(haystack, needle, n):
    """
    Find the nth needle in haystack.
    :param haystack: the string from which we want to find needle
    :param needle: the substring we want to find from haystack
    :param n: the nth occurrence should be found
    :return: The index of the nth needle in haystack. Return -1 if there is no such needle.
    """
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def add_line_number_offset(line, offset):
    """
    Offset the line number, which is located before the first semicolon.
    Example: for a line '20: error: ...' and offset 5, return '5: error: ...'
    :param line: A line of error message. Assume it always starts with number.
    :param offset: The offset of the user code.
    :return: a error message whose line number indicator is offset.
    """
    if line is None or offset is None:
        # should log this error.
        return line
    semicolon_index = line.index(':')
    if semicolon_index < 0:
        return line
    old_line_num = int(line[:semicolon_index])
    return str(old_line_num - int(offset)) + line[semicolon_index:]


def process_java_comp_err(test_code, comp_err):
    """
    Process the compilation error message, so that the user can get an accurate line number of
    error.
    We are combining the user code with test code, then run them together. The problem is that,
    when the java compiler throws an error, the line number belongs to the line in a combined file.
    The line numbers can be misleading.
    :param test_code:
    :param comp_err:
    :return: process the compiler error message.
    """
    # find the line number offset.
    # we count the number of newlines before the second '%s', where the user code is inserted.
    insertion_index = find_nth(test_code, '%s', 2)
    lines_offset = test_code[:insertion_index].count('\n')  # n lines with n - 1 newline chars.
    print 'lines_offset: ' + str(lines_offset)

    # first, find the solutions.
    print 'The comp_err is ' + comp_err
    print 'The test_code is ' + test_code
    processed_comp_err = ""
    lines = comp_err.splitlines()
    for line in lines:
        if COMP_ERR_ANCHOR in line:
            index = line.index(COMP_ERR_ANCHOR)
            useful_part = line[(index + COMP_ERR_ANCHOR_LEN):]
            useful_part_with_new_line_num = add_line_number_offset(useful_part, lines_offset)
            print 'The useful part is ' + useful_part_with_new_line_num
            processed_comp_err += useful_part_with_new_line_num
        else:
            processed_comp_err += line
        processed_comp_err += '\n'
    print 'The processed compilation err is: ' + processed_comp_err
    return processed_comp_err


# Compiles and runs code, returns a dict with status and err_msg.
def run_java_code(test_code, user_code, timeout):
    """
    Run the user code, with timeout restrictions.
    :param test_code: the test code for a problem.
    :param user_code: the user submitted code for a problem.
    :param timeout: the timeout of this problem. Unit: second.
    :return: a dictionary with the status and message.
    """
    # Write the code into a random directory.
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    rand_dir = 'dir' + str(random.randrange(0, RAND_RANGE))
    # Make sure that the rand directory doesn't exist.
    while os.path.exists(curr_dir + '/' + rand_dir):
        rand_dir += str(random.randrange(0, RAND_RANGE))
    child_dir = curr_dir + '/' + rand_dir + '/'
    clean_cmd = format(CLEAN % (curr_dir + '/' + rand_dir))
    print rand_dir
    # Make sure that the random directory is created.
    if not os.path.exists(child_dir):
        os.makedirs(child_dir)

    # Construct the source code and write it into file.
    package_info = 'package ' + rand_dir + ';'

    code = format(test_code % (package_info, user_code))
    print code
    file_path = child_dir + 'Solution.java'
    print file_path
    text_file = open(file_path, 'w')
    text_file.write(code)
    text_file.flush()
    text_file.close()

    # Attempt to compile the java code.
    comp_err_file_path = child_dir + 'comp_err'
    print comp_err_file_path
    compile_command = format(COMPILE % (file_path, comp_err_file_path))
    try:
        subprocess.check_call(compile_command, shell=True)
    except CalledProcessError:
        print 'Error compiling'
        # Read the compilation error message, and return in a dictionary.

        msg = open(comp_err_file_path, 'r').read()
        # print msg
        os.system(clean_cmd)
        return {'status': 'Compiler error',
                'message': process_java_comp_err(test_code, msg)}

    # If the file compiles successfully, attempt to run it.
    run_err_file_path = child_dir + 'run_err'
    run_target = rand_dir + '.Solution'
    run_command = format(RUN % (curr_dir, run_target, run_err_file_path))
    # Run the command. Upon timeout, kill the subprocess and return an error code.
    try:
        subp = subprocess.Popen(run_command, shell=True)
        time.sleep(timeout)
        if subp.poll() is None:  # Still running.
            print 'Still running.'
            subp.kill()
            os.system(clean_cmd)
            return {'status': 'Time Limit Exceeded', 'message': 'Be careful of the time complexity'}

        else:
            ret_code = subp.returncode
            runtime_error = open(run_err_file_path, 'r').read()
            print runtime_error

    except CalledProcessError:
        print 'Error running'
        print 'Trying to get err msg from ' + run_err_file_path
        msg = open(run_err_file_path, 'r').read()
        os.system(clean_cmd)
        return {'status': 'Runtime error', 'message': msg}

    # Return accepted or wrong answer.
    os.system(clean_cmd)
    print 'return code is: ' + str(ret_code)
    if str(ret_code) == '0':
        return {'status': 'Accepted', 'message': 'Congrats'}
    else:
        if len(runtime_error) > 0 and runtime_error.startswith('Exception'):
            return {'status': 'Runtime error', 'message': runtime_error}
        else:
            return {'status': 'Wrong answer', 'message': 'Please try again'}
