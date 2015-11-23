import urllib
import urllib2

usercode = '''
public static boolean returnFalse() {
	return true;
}
'''

testcode = '''%s
public class Solution {
	public static void main(String[] args) {
	    int ret = 1;
	    if (returnFalse() == false) {
	        ret = 0;
	    }
	    System.exit(ret);
	}
	%s
}'''

tle = 1

py_usercode = '''
def returnFalse():
    return False
'''

py_testcode = '''
import sys
%s

ret = 1
if returnFalse() == False:
    print 'Not good'
    ret = 0


sys.exit(ret)
'''

url = 'http://52.26.238.153/worker/judge'
values = {'user_code' : py_usercode,
          'test_code': py_testcode,
          'tle': tle,
          'language': 'Python'}

# data = urllib.urlencode(values)
# req = urllib2.Request(url, data)
# response = urllib2.urlopen(req)
# the_page = response.read()
# print the_page

# req = urllib2.Request(url)

data = urllib.urlencode(values)
u = urllib.urlopen("http://localhost:8000/worker/judge/?%s" % data)
print u.read()


