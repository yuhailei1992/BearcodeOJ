import multiprocessing
import time

# Your foo function
def foo(n):
    for i in range(0, n):
        print "Tick"
        time.sleep(1)


p = multiprocessing.Process(target=foo, name="Foo", args=(10,))
p.start()

p.join(10)

# If thread is active
if p.is_alive():
    print "foo is running... let's kill it..."

    # Terminate foo
    p.terminate()
    p.join()