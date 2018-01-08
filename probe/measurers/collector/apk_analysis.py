from __future__ import absolute_import
from ...runtime import runtime
from ...android.adb import adb
from ...obj.meta import SnapshotRegistrar

__author__ = 'rotem'


class ApkSize(object):
    __metaclass__ = SnapshotRegistrar
    def __init__(self):
        pass

    def name(self):
        return 'apk_size'

    def value(self):
        s = runtime.get_package_name()
        output = adb.shell('run-as {} du -s /data/data/{}'.format(s, s)).get('stdout')
        apk_size = output[0].split()[0]
        # print 'apk_size:%s' % apk_size
        return int(apk_size)

'''
class BatteryUsage(object):
    """
    Cpu usage - user space (in ticks)
    """

    __metaclass__ = SnapshotRegistrar

    def __init__(self):
        pass

    def name(self):
        """
        the key of this measurement in the output dict
        """

        return 'battery_usage'

    def value(self):
        """
        the value of this measurement in the output dict
        """

        s = runtime.get_package_name()
        output = adb.shell('dumpsys batterystats --charged {}'.format(s)).get('stdout')
        u = output[0].split()[0]
        # print 'apk_size:%s' % apk_size
        return int(u)


'''



class DexMethodCount(object):
    __metaclass__ = SnapshotRegistrar
    def __init__(self):
        self.method_count = 0

    def name(self):
        return 'apk_dex_method_count'

    def value(self):
        if self.method_count == 0:
            output = adb.exec_command('java -jar libs/dex-method-counts.jar {}'.format(adb.get_apk_path())).get('stdout')
            #print output
            count = output[-1].split(':')[1].strip()
            self.method_count = int(count)

        return self.method_count