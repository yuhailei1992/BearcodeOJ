import subprocess
from subprocess import CalledProcessError
from os import listdir
from os.path import isfile, join
import filecmp

COMPILE = 'javac %s%s.java 2> comp_err'
RUN = 'java %s > res 2> run_err'
JAVA_SUFFIX = '.java'
EXPECTED = 'expected'


def run_code(path):
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
            try:
                subprocess.check_call(run_command, shell=True)
            except CalledProcessError:
                print 'Error running'
                err_file_name = path + 'run_err'
                return {'return_code': 2, 'return_msg': open(err_file_name, 'r').read()}
            # After running, compare with expected output.
            # If the output are the same, return true; else return false.
            expected_file_name = path + EXPECTED
            res_file_name = path + 'res'
            if filecmp.cmp(expected_file_name, res_file_name):
                return {'return_code': 0, 'return_msg': 'Pass'}
            else:
                return {'return_code': 3, 'return_msg': 'Wrong answer'}

