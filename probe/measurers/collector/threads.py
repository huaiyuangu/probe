from __future__ import absolute_import
from ...runtime import runtime
from ...android.adb import adb
from ...obj.meta import SnapshotRegistrar

__author__ = 'joey'


class NumThreads(object):
    __metaclass__ = SnapshotRegistrar
    def __init__(self):
        """
        PID - Process ID
        CPU% - CPU Usage
        S - State (or possibly status) R=Running, S=Sleeping
        #THR - Number of threads
        PCY - I'm kinda stumped here. You seem to have a pretty good grasp of what it does, so that's good enough (assuming that fg and bg are the only possible values)
        UID - Name of the user that started the task
        Name - This one is self-explanatory...
        ['27704 u0_a197  10 -10   6% S   104 1535144K 153636K  fg com.hulu.debug\n']
        """
        pass

    def name(self):
        return 'num_of_threads'

    def value(self):
        output = adb.shell('top -n 1 | grep %s' % runtime.get_package_name()).get('stdout')
        #print ('%s is %s' % (self.name(), output))
        num_threads = output[0].split()[6]
        return int(num_threads)