from django.test import TestCase
from saltstack.tasks import add

# Create your tests here.

result = add.delay(2,2)

print result

if result.ready():
    print "Task has run"
    if result.successful():
        print "Result was: %s" % result.result
    else:
        if isinstance(result.result, Exception):
            print "Task failed due to raising an exception"
            raise result.result
        else:
            print "Task failed without raising exception"
else:
    print "Task has not yet run"