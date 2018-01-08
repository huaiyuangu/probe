from __future__ import absolute_import
import Queue
import time
import os
from subprocess import Popen, PIPE, STDOUT

from .android import adb
from .helpers.logger import logger
from .runtime import runtime
from .obj import classregistry
from .collector import Collector
from .android.logcat import AsyncLogcatReader
from .obj.output import ProbeOutput


__author__ = 'rotem'


class Probe():

    def __init__(self, tricorder, package, activity, device_id):
        self.stopped = False
        runtime.reset()
        runtime.package_name = package

        self.tricorder = tricorder
        self.adb = adb.adb
        self.adb.set_device_id(device_id)
        self.package_name = package
        self.probe_output = ProbeOutput()

        self.adb.kill(package)
        # cleanup logcat history before starting to collect log lines
        self.adb.logcat_clean()
        self.adb.start(package, activity)

        self.logcat = self.adb.logcat_start(package)
        self.stdout_queue = Queue.Queue()
        self.stdout_reader = AsyncLogcatReader(self.logcat, self.stdout_queue, self.package_name)

    def reset_reader(self):
        self.stdout_reader.stop()

        self.logcat = self.adb.logcat_start(runtime.package_name)
        self.stdout_reader = AsyncLogcatReader(self.logcat, self.stdout_queue, self.package_name)
        self.stdout_reader.start()

    def start(self, timeout=None):
        logger.debug('Probe listener started')
        logger.info('Listening on logcat output')
        self.stdout_reader.start()

        t0 = time.time()
        lastLine = ''

        # Check the queues if we received some output (until there is nothing more to get).
        while not self.stdout_reader.eof() and not self.stopped:
            try:
                line = self.stdout_queue.get(timeout=timeout)
                if line == lastLine:
                    raise Exception('stdout has no new output')
            except Exception as e:
                print e
                logger.info('%s\'s logcat output is silent for %d seconds, ' \
                      'Taking a snapshot with Collector now\n' % (self.package_name, timeout))
                self.reset_reader()
                continue

            if line is None:
                break

            for measurer in classregistry.continuous_registry:
                if measurer.is_matching(line):
                    measurer.process(line)

            if (time.time() - t0) > 10:
                t0 = time.time()
                logger.info('%s\'s logcat output: 10s passed, and take a snapshot with Collector now\n' % (self.package_name))
                self.collect_output()
                normalized_result = self.tricorder.dump()
                previous_results = self.tricorder.get_previous_runs(normalized_result)
                build_successful, error_log = self.tricorder.compare_with_previous_results(previous_results, normalized_result)
                self.tricorder.reset()
                # Fail if results are above the defined threshold
                if build_successful:
                    logger.info('Probe: run OK. All measurements from current in instance are within threshold bounds')
                else:
                    logger.error('Probe: run failed! Summarizing failed tests:')
                    logger.error('\n' + error_log)

        if not self.stopped:
            self.stop()

    def collect_output(self):

        collector = Collector()
        collector_output = collector.collect()

        self.tricorder.record_probe(self.probe_output)
        self.tricorder.record_collector(collector_output)

    def stop(self):
        self.stopped = True
        # Probe is the only consumer of stdout_reader, we can kill stdout_reader safely
        self.stdout_reader.stop()
        self.logcat.terminate()

        collector = Collector()
        collector_output = collector.collect()

        self.tricorder.record_probe(self.probe_output)
        self.tricorder.record_collector(collector_output)

        logger.info('Probe listener stopped {}'.format(self))

