import multiprocessing
import time
import subprocess



def multi():

    def foo():
        subprocess.check_call('sleep 10', shell=True)
    print 'timed_exec'
    p = multiprocessing.Process(target=foo, name="Foo", args=())
    p.start()

    p.join(3)

    # If thread is active
    if p.is_alive():
        print "foo is running... let's kill it..."

        # Terminate foo
        p.terminate()
        p.join()
    else:
        print 'Terminated!'

multi()