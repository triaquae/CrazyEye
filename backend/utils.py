#_*_coding:utf-8_*_
__author__ = 'jieli'

import time
import random,string
def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d %T")
    #elif isinstance(obj, ...):
    #    return obj
    #else:
    #    raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

def json_date_to_stamp(obj):
    if hasattr(obj, 'isoformat'):
        return time.mktime(obj.timetuple()) *1000



def random_str(length):
    '''generate randome string'''
    source = string.ascii_lowercase + string.digits
    rand_str = random.sample(source,length)
    return ''.join(rand_str)

#print(random_str(16))