try:
    import ltihooks
except:
    pass

import _gtksheet
from _gtksheet import *

# Allow other modules to install data handlers for arbitrary types.
#
# Handler must return a tuple (obj, buffer, buffer_len) of types
# (PyObject, Long, Int).
#
# Look at the C code for details of exactly what happens.
#
# The 'obj' PyObject will be stored in the data set until
# set to something else or the data set is destroyed.
# 
# You must take responsibility for life of the obj and ensure
# that the buffer and buffer_len do not change unless
# you call set_points() again before they are used.

"""
_handlers  = []
def add_handler( handler ):
    _handlers.insert(0, handler)

def _data_from_pyobject_callback(obj):
    for h in _handlers:
        r = h(obj)
        if not r is None:
            return r
    raise TypeError('No handler installed for type %s' % type(obj))
_gtksheet._set_data_from_pyobject_callback(_data_from_pyobject_callback)


def _array_handler( obj ):
    "Data handler array.array's and any sequence of numbers including lists of numbers."
    import array
    if type(obj) is array.ArrayType:
        a = obj
    else:
        a = array.array('d', obj)
    return (a,) + a.buffer_info()


add_handler( _array_handler )
"""
