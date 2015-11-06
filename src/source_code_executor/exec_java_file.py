import subprocess
from subprocess import CalledProcessError
import filecmp, time, os


COMPILE = 'javac %s 2> %s'
RUN = 'exec java %s 2> %s'

SKELETON = '''
%s
public class Solution {
    public static void main(String[] args) {
        int ret = 1; // Assume wrong answer.
        if (1 == foo(1) && 2 == foo(2)) {
            ret = 100;
        }
        System.exit(ret);
    }

    %s
}
'''

FUNCTION = '''
    public static int foo(int x) {
        return x;
    }
'''

# Compiles and runs code, returns a dict with return_code and err_msg.
# return_code: 0 - Accepted; 1 - Compiler error; 2 - Runtime error; 3 - Wrong answer; 4 - TLE.
def run_code(path, timeout):
    # Write the code into a random directory.

    # Get all the necessary information, such as folder name, class name, etc.
    DIR = 'p2333'
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    child_dir = curr_dir + '/' + DIR + '/'
    package_info = 'package ' + DIR + ';'
    # Ensure that the random directory exists.
    if not os.path.exists(child_dir):
        os.makedirs(child_dir)
    file_path = child_dir + 'Solution.java'
    text_file = open(file_path, 'w')
    text_file.write(SKELETON % (package_info, FUNCTION))
    text_file.close()

    comp_target = DIR + '/' + 'Solution.java'
    comp_err_file_path = child_dir + 'comp_err'
    # Attempt to compile it.
    compile_command = format(COMPILE % (comp_target, comp_err_file_path))
    print 'the compile_command is'
    print compile_command
    try:
        subprocess.check_call(compile_command, shell=True)
    except CalledProcessError:
        print 'Error compiling'
        # Read the compilation error message, and return in a dictionary.
        return {'return_code': 1, 'return_msg': open(comp_err_file_path, 'r').read()}

    # If the file compiles successfully, attempt to run it.
    run_err_file_path = child_dir + 'run_err'
    run_target = DIR + '.Solution'
    run_command = format(RUN % (run_target, run_err_file_path))

    print 'the run command is'
    print run_command

    # Run the command. Upon timeout, kill the subprocess and return an error code.
    try:
        subp = subprocess.Popen(run_command, shell=True)
        time.sleep(timeout)
        if not subp.poll(): # Still running.
            print 'Still running'
            subp.kill()
            return {'return_code': 4, 'return_msg': 'Time Limit Exceeded'}
        else:
            print 'The return code is ' + str(subp.returncode)
            print 'Already stopped'

    except CalledProcessError:
        print 'Error running'
        return {'return_code': 2, 'return_msg': open(run_err_file_path, 'r').read()}
    # After running, compare with expected output.
    return {'return_code': 3, 'return_msg': 'Wrong answer'}

