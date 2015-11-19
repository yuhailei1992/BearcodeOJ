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


# Compiles and runs code, returns a dict with status and err_msg.
def run_java_code(test_code, user_code, timeout):
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

    # Attempt to compile the source code.
    comp_err_file_path = child_dir + 'comp_err'
    print comp_err_file_path
    compile_command = format(COMPILE % (file_path, comp_err_file_path))
    try:
        subprocess.check_call(compile_command, shell=True)
    except CalledProcessError:
        print 'Error compiling'
        # Read the compilation error message, and return in a dictionary.

        msg = open(comp_err_file_path, 'r').read()
        print msg
        os.system(clean_cmd)
        return {'status': 'Compiler error', 'message': msg}

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
            # print 'The return code is ' + str(subp.returncode)
            ret_code = subp.returncode

    except CalledProcessError:
        print 'Error running'
        print 'Trying to get err msg from ' + run_err_file_path
        msg = open(run_err_file_path, 'r').read()
        os.system(clean_cmd)
        return {'status': 'Runtime error', 'message': msg}

    # Return accepted or wrong answer.
    os.system(clean_cmd)
    print 'return code is' + str(ret_code)
    if str(ret_code) == '0':
        return {'status': 'Accepted', 'message': 'Congrats'}
    else:
        return {'status': 'Wrong answer', 'message': 'Please try again'}

