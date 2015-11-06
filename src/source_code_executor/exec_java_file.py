import multiprocessing
import subprocess
from subprocess import CalledProcessError
from os import listdir
from os.path import isfile, join
import filecmp, time


COMPILE = 'javac %s%s.java 2> comp_err'
RUN = 'exec java %s > res 2> run_err'
JAVA_SUFFIX = '.java'
EXPECTED = 'expected'


# Compiles and runs code, returns a dict with return_code and err_msg.
# return_code: 0 - Accepted; 1 - Compiler error; 2 - Runtime error; 3 - Wrong answer; 4 - TLE.
def run_code(path, timeout):
    # Parameter sanity check.
    if not path or len(path) == 0:
        raise ValueError("Invalid path")

    # List all the files under path.
    filenames = [f for f in listdir(path) if isfile(join(path, f))]
    # Execute the first .java file.
    for filename in filenames:
        if filename.endswith(JAVA_SUFFIX):
            class_name = filename[:-5]
            # Attempt to compile it.
            compile_command = format(COMPILE % (path, class_name))
            try:
                subprocess.check_call(compile_command, shell=True)
            except CalledProcessError:
                print 'Error compiling'
                # Read the compilation error message, and return in a dictionary.
                err_file_name = path + 'comp_err'
                return {'return_code': 1, 'return_msg': open(err_file_name, 'r').read()}

            # If the file compiles successfully, attempt to run it.
            run_command = format(RUN % class_name)
            def run_java_code():
                print 'Trying to run the command: ' + run_command
                subp = subprocess.Popen(run_command, shell=True)
                subp.wait()

            # Run the command. Upon timeout, kill the subprocess and return an error code.
            try:
                subp = subprocess.Popen(run_command, shell=True)
                time.sleep(timeout)
                if not subp.poll():
                    print 'Still running'
                    subp.kill()
                    return {'return_code': 4, 'return_msg': 'Time Limit Exceeded'}
                else:
                    print 'Already stopped'

            except CalledProcessError:
                print 'Error running'
                err_file_name = path + 'run_err'
                return {'return_code': 2, 'return_msg': open(err_file_name, 'r').read()}
            # After running, compare with expected output.
            expected_file_name = path + EXPECTED
            res_file_name = path + 'res'
            if filecmp.cmp(expected_file_name, res_file_name):
                return {'return_code': 0, 'return_msg': 'Pass'}
            else:
                return {'return_code': 3, 'return_msg': 'Wrong answer'}

