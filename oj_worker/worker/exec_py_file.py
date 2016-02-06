import subprocess
from subprocess import CalledProcessError
import random
import os
import time

# Need to cd to the working directory, then call java to execute the .class file.
RUN = 'cd %s && exec python %s 2> %s'
RAND_RANGE = 100000000
CLEAN = 'rm -r %s'


# Compiles and runs code, returns a dict with status and err_msg.
def run_py_code(test_code, user_code, timeout):
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
    code = format(test_code % (user_code))
    print code

    # Write the code into file.
    file_path = child_dir + 'solution.py'
    print file_path
    text_file = open(file_path, 'w')
    text_file.write(code)
    text_file.flush()
    text_file.close()

    # Run the python code.
    run_err_file_path = child_dir + 'run_err'
    target_dir = curr_dir + '/' + rand_dir
    run_target = 'solution.py'
    run_command = format(RUN % (target_dir, run_target, run_err_file_path))
    print run_command
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
            print 'The return code is ' + str(subp.returncode)
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

