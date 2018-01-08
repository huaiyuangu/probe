from probe.probe import Probe
from probe.tricorder import Tricorder
from unittest import TestCase

from unittest import TestCase
import unittest


class PerformanceTestCase(TestCase):
    probe = None
    package = 'com.hulu.debug'
    activity = 'com.hulu.features.splash.SplashActivity'
    device_id = 'ZX1G22CWGP'

    def setup_method(self, method):
        super(PerformanceTestCase, self).setup_method(method)


    def test_playback(self):
        self.probe = Probe(Tricorder(self.package), self.package, self.activity, self.device_id)
        self.probe.start(timeout=60)
        pass
        self.probe.stop()
        # manually

    def teardown_method(self, method):
        super(PerformanceTestCase, self).teardown_method(method)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PerformanceTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)