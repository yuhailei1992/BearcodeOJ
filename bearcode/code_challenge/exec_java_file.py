__author__ = 'cissy'

import subprocess
from subprocess import CalledProcessError
import random, time, os

COMPILE = 'javac %s 2> %s'
# Need to cd to the working directory, then call java to execute the .class file.
RUN = 'cd %s && exec java %s 2> %s'
RAND_RANGE = 100000000
CLEAN = 'rm -r %s'


# Compiles and runs code, returns a dict with return_code and err_msg.
# return_code: 0 - Accepted; 1 - Compiler error; 2 - Runtime error; 3 - Wrong answer; 4 - TLE.
def run_code(test_code, user_code, timeout):
    # Write the code into a random directory.
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    rand_dir = 'dir' + str(random.randrange(0, RAND_RANGE))
    # Make sure that the rand directory doesn't exist.
    while os.path.exists(curr_dir + '/' + rand_dir):
        rand_dir = rand_dir + str(random.randrange(0, RAND_RANGE))
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
    compile_command = format(COMPILE % (file_path, comp_err_file_path))
    try:
        subprocess.check_call(compile_command, shell=True)
    except CalledProcessError:
        print 'Error compiling'
        # Read the compilation error message, and return in a dictionary.
        os.system(clean_cmd)
        return {'return_code': 1, 'return_msg': open(comp_err_file_path, 'r').read()}

    # If the file compiles successfully, attempt to run it.
    run_err_file_path = child_dir + 'run_err'
    run_target = rand_dir + '.Solution'
    run_command = format(RUN % (curr_dir, run_target, run_err_file_path))
    # Run the command. Upon timeout, kill the subprocess and return an error code.
    try:
        subp = subprocess.Popen(run_command, shell=True)
        time.sleep(timeout)
        ret_code = -1
        if subp.poll() is None: # Still running.
            print 'Still running.'
            subp.kill()
            os.system(clean_cmd)
            return {'return_code': 4, 'return_msg': 'Time Limit Exceeded'}

        else:
            # print 'The return code is ' + str(subp.returncode)
            ret_code = subp.returncode

    except CalledProcessError:
        print 'Error running'
        os.system(clean_cmd)
        return {'return_code': 2, 'return_msg': open(run_err_file_path, 'r').read()}

    # Return accepted or wrong answer.
    os.system(clean_cmd)
    print 'return code is' + str(ret_code)
    if str(ret_code) == '0':
        return {'return_code': 0, 'return_msg': 'Accepted'}
    else:
        return {'return_code': 3, 'return_msg': 'Wrong answer'}

