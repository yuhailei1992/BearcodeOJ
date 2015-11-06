from exec_java_file import run_code
import subprocess

PATH = '/Users/Caesar/Documents/workspace/Team142/src/source_code_executor/'

def exec_java_file_test():
    print 'Exec java file test...'
    # subprocess.check_call('sleep 1', shell=True)
    res = run_code(path=PATH, timeout=20)
    print 'The result is' + str(res)

exec_java_file_test()
