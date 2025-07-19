#!/usr/bin/env python

import logging
import multiprocessing as mp
import os
import unittest
from multiprocessing import Queue
from multiprocessing.queues import Empty
from time import sleep, time

import numpy as np

from openfilter.filter_runtime import Filter, FilterConfig, Frame
from openfilter.filter_runtime.test import RunnerContext, FiltersToQueue, QueueToFilters
from openfilter.filter_runtime.utils import setLogLevelGlobal
from openfilter.filter_runtime.filters.util import Util

logger = logging.getLogger(__name__)

log_level = int(getattr(logging, (os.getenv('LOG_LEVEL') or 'CRITICAL').upper()))

setLogLevelGlobal(log_level)

getdatas = lambda q, t=5: {t: f.data for t, f in q.get(True, t).items()}


class FilterFromQueue(Filter):
    def setup(self, config):
        if (start_sleep := config.start_sleep):
            sleep(start_sleep)

    def process(self, frames):
        if (frames := self.config.queue.get()) is None:
            self.exit()

        sleep(self.config.sleep or 0)

        return {t: Frame(d) for t, d in frames.items()}


class FilterToQueue(Filter):
    def setup(self, config):
        if (start_sleep := config.start_sleep):
            sleep(start_sleep)

    def process(self, frames):
        self.config.queue.put(frames)

        sleep(self.config.sleep or 0)


class TestFilterOld(unittest.TestCase):
    """Old doesn't mean invalid, just that it was written before some features that would have made these tests simpler
     and different if written today. Many of these are only 99.9% deterministic because of network entropy so if they
     fail treat them as a screen rather than definitive invalidation and try again."""

    def test_topo_simple(self):
        qout = Queue(); [qout.put({'main': {'count': i}}) for i in range(5)]; qout.put(None)

        retcodes = Filter.run_multi([
            (FilterFromQueue, dict(outputs='tcp://*', queue=qout, sleep_start=0.5, sleep=0.05)),
            (FilterToQueue,   dict(sources='tcp://127.0.0.1', queue=(qin := Queue()))),
        ], exit_time=10)

        self.assertEqual(retcodes, [0, 0])

        self.assertEqual({t: f.data for t, f in qin.get(0).items()}, {'main': {'count': 0}})
        self.assertEqual({t: f.data for t, f in qin.get(0).items()}, {'main': {'count': 1}})
        self.assertEqual({t: f.data for t, f in qin.get(0).items()}, {'main': {'count': 2}})
        self.assertEqual({t: f.data for t, f in qin.get(0).items()}, {'main': {'count': 3}})
        self.assertEqual({t: f.data for t, f in qin.get(0).items()}, {'main': {'count': 4}})


    def test_topo_tee(self):
        qout = Queue(); [qout.put({'main': {'count': i}}) for i in range(5)]; qout.put(None)

        retcodes = Filter.run_multi([
            (FilterFromQueue, dict(outputs='tcp://*', outputs_required='1, 2', queue=qout, sleep_start=0.5, sleep=0.5)),  # the sleeps because might miss published messages at startup
            (FilterToQueue,   dict(id='1', sources='tcp://127.0.0.1', queue=(qin1 := Queue()))),
            (FilterToQueue,   dict(id='2', sources='tcp://127.0.0.1', queue=(qin2 := Queue()))),
        ], exit_time=10)

        self.assertEqual(retcodes, [0, 0, 0])

        self.assertEqual({t: f.data for t, f in qin1.get(0).items()}, {'main': {'count': 0}})
        self.assertEqual({t: f.data for t, f in qin1.get(0).items()}, {'main': {'count': 1}})
        self.assertEqual({t: f.data for t, f in qin1.get(0).items()}, {'main': {'count': 2}})
        self.assertEqual({t: f.data for t, f in qin1.get(0).items()}, {'main': {'count': 3}})
        self.assertEqual({t: f.data for t, f in qin1.get(0).items()}, {'main': {'count': 4}})

        self.assertEqual({t: f.data for t, f in qin2.get(0).items()}, {'main': {'count': 0}})
        self.assertEqual({t: f.data for t, f in qin2.get(0).items()}, {'main': {'count': 1}})
        self.assertEqual({t: f.data for t, f in qin2.get(0).items()}, {'main': {'count': 2}})
        self.assertEqual({t: f.data for t, f in qin2.get(0).items()}, {'main': {'count': 3}})
        self.assertEqual({t: f.data for t, f in qin2.get(0).items()}, {'main': {'count': 4}})


    def test_topo_tee_rejoin(self):
        qout = Queue(); [qout.put({'main': {'count': i}}) for i in range(5)]; qout.put(None)

        retcodes = Filter.run_multi([
            (FilterFromQueue, dict(id='src', outputs='tcp://*', outputs_required='1, 2', queue=qout, sleep_start=0.5, sleep=0.5)),  # the sleeps because might miss published messages at startup
            (Util,            dict(id='1',   sources='tcp://127.0.0.1', outputs='tcp://*:5552', outputs_required='out')),
            (Util,            dict(id='2',   sources='tcp://127.0.0.1', outputs='tcp://*:5554', outputs_required='out')),
            (FilterToQueue,   dict(id='out', sources='tcp://127.0.0.1:5552, tcp://127.0.0.1:5554;>other', queue=(queue := Queue()))),
        ], exit_time=10)

        self.assertEqual(retcodes, [0, 0, 0, 0])

        self.assertEqual({t: f.data for t, f in queue.get(0).items()}, {'main': {'count': 0}, 'other': {'count': 0}})
        self.assertEqual({t: f.data for t, f in queue.get(0).items()}, {'main': {'count': 1}, 'other': {'count': 1}})
        self.assertEqual({t: f.data for t, f in queue.get(0).items()}, {'main': {'count': 2}, 'other': {'count': 2}})
        self.assertEqual({t: f.data for t, f in queue.get(0).items()}, {'main': {'count': 3}, 'other': {'count': 3}})
        self.assertEqual({t: f.data for t, f in queue.get(0).items()}, {'main': {'count': 4}, 'other': {'count': 4}})


    def test_topo_ephemeral_simple(self):
        qout = Queue(); [qout.put({'main': {'count': i}}) for i in range(8)]; qout.put(None)

        retcodes = Filter.run_multi([
            (FilterFromQueue, dict(outputs='tcp://*', queue=qout, sleep=0.01)),
            (FilterToQueue, dict(sources='tcp://127.0.0.1?', queue=(queue := Queue()))),
        ], exit_time=10)

        self.assertEqual(retcodes, [0, 0])

        self.assertEqual({t: f.data for t, f in queue.get(0).items()}, {'main': {'count': 0}})
        self.assertEqual({t: f.data for t, f in queue.get(0).items()}, {'main': {'count': 1}})
        self.assertEqual({t: f.data for t, f in queue.get(0).items()}, {'main': {'count': 2}})
        self.assertEqual({t: f.data for t, f in queue.get(0).items()}, {'main': {'count': 3}})
        self.assertEqual({t: f.data for t, f in queue.get(0).items()}, {'main': {'count': 4}})


    def test_topo_ephemeral_tee(self):
        qout = Queue(); [qout.put({'main': {'count': i}, **({} if i & 1 else {'other': {'count': i}})}) for i in range(5)]; qout.put(None)

        retcodes = Filter.run_multi([
            (FilterFromQueue, dict(outputs='tcp://*', queue=qout, start_sleep=0.1, sleep=0.05)),
            (FilterToQueue,   dict(sources='tcp://127.0.0.1', queue=(qin1 := Queue()))),
            (FilterToQueue,   dict(sources='tcp://127.0.0.1?;other', queue=(qin2 := Queue()))),
        ], exit_time=10)

        self.assertEqual(retcodes, [0, 0, 0])

        self.assertEqual({t: f.data for t, f in qin1.get(0).items()}, {'main': {'count': 0}, 'other': {'count': 0}})
        self.assertEqual({t: f.data for t, f in qin1.get(0).items()}, {'main': {'count': 1}})
        self.assertEqual({t: f.data for t, f in qin1.get(0).items()}, {'main': {'count': 2}, 'other': {'count': 2}})
        self.assertEqual({t: f.data for t, f in qin1.get(0).items()}, {'main': {'count': 3}})
        self.assertEqual({t: f.data for t, f in qin1.get(0).items()}, {'main': {'count': 4}, 'other': {'count': 4}})

        self.assertEqual({t: f.data for t, f in qin2.get(0).items()}, {'other': {'count': 0}})
        self.assertEqual({t: f.data for t, f in qin2.get(0).items()}, {'other': {'count': 2}})
        self.assertEqual({t: f.data for t, f in qin2.get(0).items()}, {'other': {'count': 4}})


    # WARNING! `prop_exit` and `stop_exit` are temporary hacks for exit control in this case, they should be made more determiniztic.
    def test_topo_ephemeral_tee_rejoin(self):
        qout = Queue(); [qout.put({'main': {'count': i}, **({} if i & 1 or i > 4 else {'other': {'count': i}})}) for i in range(8)]; qout.put(None)

        retcodes = Filter.run_multi([
            (FilterFromQueue, dict(id='src', outputs='tcp://*', outputs_required='u0, u1', queue=qout, start_sleep=0.1, sleep=0.08)),
            (Util,            dict(id='u0',  sources='tcp://127.0.0.1;', outputs='tcp://*:5552', outputs_required='dst')),
            (Util,            dict(id='u1',  sources='tcp://127.0.0.1?;other', outputs='tcp://*:5554', outputs_required='dst')),
            (FilterToQueue,   dict(id='dst', sources='tcp://127.0.0.1:5552, tcp://127.0.0.1:5554?', queue=(qin := Queue()))),
        ], prop_exit='none', stop_exit='all', exit_time=10)

        self.assertEqual(retcodes, [0, 0, 0, 0])

        msgs = set()

        for _ in range(9):
            try:
                msgs.update(f'{t}{f.data["count"]}' for t, f in qin.get(0).items())
            except Empty:
                pass

        self.assertEqual(msgs, set(('main0', 'main5', 'main4', 'main7', 'main3', 'main6', 'other0', 'main1', 'other2', 'other4', 'main2')))


    def test_topo_ephemeral_join_step(self):
        qout1, qout2 = Queue(), Queue()

        runner = Filter.Runner([
            (FilterFromQueue, dict(id='inc', outputs='tcp://*:5550', queue=qout1, start_sleep=0.1, sleep=0.02)),
            (FilterFromQueue, dict(id='ine', outputs='tcp://*:5552', queue=qout2, start_sleep=0.1, sleep=0.02)),
            (FilterToQueue,   dict(id='out', sources='tcp://127.0.0.1:5550, tcp://127.0.0.1:5552?', queue=(qin := Queue()))),
        ], prop_exit='all', stop_exit='all', sig_stop=False, exit_time=10)

        try:
            qout1.put(d := {'main': {'val': 0}})

            sleep(0.05)

            self.assertIs(runner.step(), False)
            self.assertEqual(getdatas(qin), d)

            qout2.put(e := {'other': {'val': 1}})

            sleep(0.05)

            self.assertIs(runner.step(), False)
            self.assertRaises(Empty, lambda: getdatas(qin, 0.05))

            qout1.put(d := {'main': {'val': 1}})

            sleep(0.05)

            self.assertIs(runner.step(), False)
            self.assertEqual(getdatas(qin), {**d, **e})

            qout1.put(d := {'main': {'val': 2}})

            sleep(0.05)

            self.assertIs(runner.step(), False)
            self.assertEqual(getdatas(qin), d)

            qout2.put(e := {'other': {'val': 3}})

            sleep(0.05)

            self.assertIs(runner.step(), False)
            self.assertRaises(Empty, lambda: getdatas(qin, 0.05))

            qout1.put(d := {'main': {'val': 3}})

            sleep(0.05)

            self.assertIs(runner.step(), False)
            self.assertEqual(getdatas(qin), {**d, **e})

            qout2.put(e := {'other': {'val': 4}})

            sleep(0.05)

            self.assertIs(runner.step(), False)
            self.assertRaises(Empty, lambda: getdatas(qin, 0.05))

            qout1.put(d := {'main': {'val': 4}})

            sleep(0.05)

            self.assertIs(runner.step(), False)
            self.assertEqual(getdatas(qin), {**d, **e})

            qout1.put(None)  # tell them nicely to stop
            qout2.put(None)
            self.assertEqual(runner.step(), [0, 0, 0])

        finally:
            runner.stop()


    def test_topo_doubly_ephemeral_tee_step(self):
        runner1 = Filter.Runner([
            (FilterFromQueue, dict(outputs='tcp://*', queue=(qout := Queue()), start_sleep=0.1)),
            (FilterToQueue,   dict(sources='tcp://127.0.0.1??', queue=(qin1 := Queue()))),
        ], exit_time=10)

        try:
            sleep(0.2)

            qout.put(d := {'main': {'val': 0}})
            self.assertIs(runner1.step(), False)

            sleep(0.1)

            self.assertRaises(Empty, lambda: getdatas(qin1, 0.1))

            runner2 = Filter.Runner([
                (FilterToQueue, dict(sources='tcp://127.0.0.1?', queue=(qin2 := Queue()))),
            ], exit_time=10)

            try:
                self.assertIs(runner2.step(), False)

                sleep(0.1)

                self.assertEqual(getdatas(qin2), d)
                self.assertEqual(getdatas(qin1), d)

                qout.put(d := {'main': {'val': 1}})
                self.assertIs(runner1.step(), False)
                self.assertIs(runner2.step(), False)

                sleep(0.1)

                self.assertEqual(getdatas(qin2), d)
                self.assertEqual(getdatas(qin1), d)

                qout.put(None)  # tell it nicely to stop
                self.assertEqual(runner2.step(), [0])

            finally:
                runner2.stop()

            self.assertEqual(runner1.step(), [0, 0])

        finally:
            runner1.stop()


    def test_topo_subscribe_wildcard_all_step(self):
        runner = Filter.Runner([
            (FilterFromQueue, dict(id='inc', outputs='tcp://*:5550', queue=(qout := Queue()), start_sleep=0.1, sleep=0.01)),
            (FilterToQueue,   dict(id='out', sources='tcp://127.0.0.1:5550;*', queue=(qin := Queue()))),
        ], prop_exit='all', stop_exit='all', sig_stop=False, exit_time=10)

        try:
            qout.put(d := {'main': {'val': 0}})
            self.assertIs(runner.step(), False)
            r = getdatas(qin)
            self.assertEqual(r['main'], d['main'])
            self.assertEqual(set(r), set(('main', '_metrics')))

            qout.put(d := {'main': {'val': 1}})
            self.assertIs(runner.step(), False)
            r = getdatas(qin)
            self.assertEqual(r['main'], d['main'])
            self.assertEqual(set(r), set(('main', '_metrics')))

            qout.put(d := {'main': {'val': 2}})
            self.assertIs(runner.step(), False)
            r = getdatas(qin)
            self.assertEqual(r['main'], d['main'])
            self.assertEqual(set(r), set(('main', '_metrics')))

            qout.put(None)  # tell it nicely to stop
            self.assertEqual(runner.step(), [0, 0])

        finally:
            runner.stop()


    def test_topo_balance_step(self):
        class MyFilter(Filter):
            def process(self, frames):
                self.config.queue.put(frames)

                return frames

        runner = Filter.Runner([
            (FilterFromQueue, dict(id='src', outputs='tcp://*:5550, tcp://*:5552, tcp://*:5554', outputs_balance=True, queue=(qout := Queue()), start_sleep=0.1)),
            (MyFilter,        dict(id='worker1', sources='tcp://localhost:5550', outputs='tcp://*:5560', queue=(qworker1 := Queue()))),
            (MyFilter,        dict(id='worker2', sources='tcp://localhost:5552', outputs='tcp://*:5562', queue=(qworker2 := Queue()))),
            (MyFilter,        dict(id='worker3', sources='tcp://localhost:5554', outputs='tcp://*:5564', queue=(qworker3 := Queue()))),
            (FilterToQueue,   dict(id='out', sources='tcp://127.0.0.1:5560, tcp://127.0.0.1:5562, tcp://127.0.0.1:5564', sources_balance=True, queue=(qin := Queue()))),
        ], prop_exit='all', stop_exit='all', sig_stop=False, exit_time=10)

        last_qworker = None

        def getworkerdatas():  # because order is not guaranteed
            nonlocal last_qworker

            self.assertEqual((qe1 := qworker1.empty()) + (qe2 := qworker2.empty()) + (qe3 := qworker3.empty()), 2)

            qworker = qworker1 if qe2 and qe3 else qworker2 if qe1 and qe3 else qworker3

            self.assertIsNot(qworker, last_qworker)

            last_qworker = qworker

            return getdatas(qworker)

        try:
            qout.put(d := {'main': {'val': 0}})
            self.assertIs(runner.step(), False)
            self.assertIs(runner.step(), False)

            sleep(0.05)

            self.assertEqual(getdatas(qin), d)
            self.assertEqual(getworkerdatas(), d)
            # self.assertEqual(getdatas(qworker1), d)
            # self.assertTrue(qworker2.empty())
            # self.assertTrue(qworker3.empty())

            qout.put(d := {'main': {'val': 1}})
            self.assertIs(runner.step(), False)
            self.assertIs(runner.step(), False)

            sleep(0.05)

            self.assertEqual(getdatas(qin), d)
            self.assertEqual(getworkerdatas(), d)
            # self.assertEqual(getdatas(qworker2), d)
            # self.assertTrue(qworker1.empty())
            # self.assertTrue(qworker3.empty())

            qout.put(d := {'main': {'val': 2}})
            self.assertIs(runner.step(), False)
            self.assertIs(runner.step(), False)

            sleep(0.05)

            self.assertEqual(getdatas(qin), d)
            self.assertEqual(getworkerdatas(), d)
            # self.assertEqual(getdatas(qworker3), d)
            # self.assertTrue(qworker1.empty())
            # self.assertTrue(qworker2.empty())

            qout.put(d := {'main': {'val': 3}})
            self.assertIs(runner.step(), False)
            self.assertIs(runner.step(), False)

            sleep(0.05)

            self.assertEqual(getdatas(qin), d)
            self.assertEqual(getworkerdatas(), d)
            # self.assertEqual(getdatas(qworker1), d)
            # self.assertTrue(qworker2.empty())
            # self.assertTrue(qworker3.empty())

            qout.put(d := {'main': {'val': 4}})
            self.assertIs(runner.step(), False)
            self.assertIs(runner.step(), False)

            sleep(0.05)

            self.assertEqual(getdatas(qin), d)
            self.assertEqual(getworkerdatas(), d)
            # self.assertEqual(getdatas(qworker2), d)
            # self.assertTrue(qworker1.empty())
            # self.assertTrue(qworker3.empty())

            qout.put(d := {'main': {'val': 5}})
            self.assertIs(runner.step(), False)
            self.assertIs(runner.step(), False)

            sleep(0.05)

            self.assertEqual(getdatas(qin), d)
            self.assertEqual(getworkerdatas(), d)
            # self.assertEqual(getdatas(qworker3), d)
            # self.assertTrue(qworker1.empty())
            # self.assertTrue(qworker2.empty())

            qout.put(d := {'main': {'val': 6}})
            self.assertIs(runner.step(), False)
            self.assertIs(runner.step(), False)

            sleep(0.05)

            self.assertEqual(getdatas(qin), d)
            self.assertEqual(getworkerdatas(), d)
            # self.assertEqual(getdatas(qworker1), d)
            # self.assertTrue(qworker2.empty())
            # self.assertTrue(qworker3.empty())

            qout.put(d := {'main': {'val': 7}})
            self.assertIs(runner.step(), False)
            self.assertIs(runner.step(), False)

            sleep(0.05)

            self.assertEqual(getdatas(qin), d)
            self.assertEqual(getworkerdatas(), d)
            # self.assertEqual(getdatas(qworker2), d)
            # self.assertTrue(qworker1.empty())
            # self.assertTrue(qworker3.empty())

            qout.put(d := {'main': {'val': 8}})
            self.assertIs(runner.step(), False)
            self.assertIs(runner.step(), False)

            sleep(0.05)

            self.assertEqual(getdatas(qin), d)
            self.assertEqual(getworkerdatas(), d)
            # self.assertEqual(getdatas(qworker3), d)
            # self.assertTrue(qworker1.empty())
            # self.assertTrue(qworker2.empty())

            qout.put(None)  # tell it nicely to stop
            self.assertEqual(runner.step(), [0, 0, 0, 0, 0])

        finally:
            runner.stop()


class TestFilter(unittest.TestCase):
    def test_normalize_config(self):
        scfg = dict(
            id                  = 'filter',
            sources             = 'tcp://localhost:5552;main, ipc://myipcin;other',
            sources_balance     = True,
            sources_timeout     = 100,
            sources_low_latency = True,
            outputs             = 'tcp://*:5554; ipc://myipcout',
            outputs_balance     = True,
            outputs_timeout     = 200,
            outputs_required    = 'filter1, filter2',
            outputs_metrics     = 'tcp://*:5554',
            outputs_jpg         = False,
            exit_after          = '@2024-09-17T06:26:20.189123-04:00',
            environment         = 'production',
            log_path            = 'logs',
            metrics_interval    = 120,
            extra_metrics       = [('my_int_metric', 1), ('my_str_metric', 'str')],
            mq_log              = 'pretty',
            mq_msgid_sync       = False,
        )

        dcfg = FilterConfig(
            id                  = 'filter',
            sources             = ['tcp://localhost:5552;main', 'ipc://myipcin;other'],
            sources_balance     = True,
            sources_timeout     = 100,
            sources_low_latency = True,
            outputs             = ['tcp://*:5554; ipc://myipcout'],
            outputs_balance     = True,
            outputs_timeout     = 200,
            outputs_required    = ['filter1', 'filter2'],
            outputs_metrics     = 'tcp://*:5554',
            outputs_jpg         = False,
            exit_after          = '@2024-09-17T06:26:20.189123-04:00',
            environment         = 'production',
            log_path            = 'logs',
            metrics_interval    = 120,
            extra_metrics       = {'my_int_metric': 1, 'my_str_metric': 'str'},
            mq_log              = 'pretty',
            mq_msgid_sync       = False,
        )

        ncfg1 = Filter.normalize_config(scfg)
        ncfg2 = Filter.normalize_config(ncfg1)

        self.assertIsInstance(ncfg1, FilterConfig)
        self.assertIsInstance(ncfg2, FilterConfig)
        self.assertEqual(ncfg1, dcfg)
        self.assertEqual(ncfg1, ncfg2)


    def test_process_return_none(self):
        class SendCountOrNone(Filter):
            def setup(self, config):
                self.count = -1

            def process(self, frames):
                if (count := self.count + 1) == 4:
                    self.exit()

                self.count = count

                return None if count & 1 else Frame({'count': count})

        with RunnerContext([
            (SendCountOrNone, dict(
                outputs = 'ipc://test-filter',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-filter',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], [queue], exit_time=3) as runner:

            self.assertTrue(queue.get()['main'].data == {'count': 0})
            self.assertTrue(queue.get()['main'].data == {'count': 2})
            self.assertFalse(queue.get())
            self.assertEqual(runner.wait(), [0, 0])


    def test_process_return_none_callback(self):
        class SendCountOrNoneCB(Filter):
            def setup(self, config):
                self.count = -1

            def process(self, frames):
                if (count := self.count + 1) == 4:
                    self.exit()

                self.count = count

                return lambda: None if count & 1 else Frame({'count': count})

        with RunnerContext([
            (SendCountOrNoneCB, dict(
                outputs = 'ipc://test-filter',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-filter',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], [queue], exit_time=3) as runner:

            self.assertTrue(queue.get()['main'].data == {'count': 0})
            self.assertTrue(queue.get()['main'].data == {'count': 2})
            self.assertFalse(queue.get())
            self.assertEqual(runner.wait(), [0, 0])


    def test_metrics_topic_subscribe(self):
        with RunnerContext([
            (QueueToFilters, dict(
                outputs = 'ipc://test-Q2F',
                queue   = (qin := mp.Queue()),
            )),
            (Util, dict(
                sources = 'ipc://test-Q2F',
                outputs = 'ipc://test-util',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-util;_metrics',
                queue   = (qout := FiltersToQueue.Queue()).child_queue,
            )),
        ], [qin, qout], exit_time=3) as runner:

            qin.put({'main': Frame(np.zeros((100, 160, 3)), {'meta': {'ts': time()}}, 'BGR')})
            qin.put(False)

            frames = qout.get()

            self.assertTrue(metrics := frames.get('_metrics'))

            keys = set(metrics.data.keys())

            self.assertIn('ts', keys)  # we don't test for correctness, just that they are there
            self.assertIn('fps', keys)
            self.assertIn('cpu', keys)
            self.assertIn('mem', keys)
            self.assertIn('lat_in', keys)
            self.assertIn('lat_out', keys)
            self.assertIn('uptime_count', keys)
            self.assertIn('frame_count', keys)
            self.assertIn('megapx_count', keys)

            self.assertFalse(qout.get())
            self.assertEqual(runner.wait(), [0, 0, 0])


    def test_metrics_topic_wildcard(self):
        with RunnerContext([
            (QueueToFilters, dict(
                outputs = 'ipc://test-Q2F',
                queue   = (qin := mp.Queue()),
            )),
            (Util, dict(
                sources = 'ipc://test-Q2F',
                outputs = 'ipc://test-util',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-util;*',
                queue   = (qout := FiltersToQueue.Queue()).child_queue,
            )),
        ], [qin, qout], exit_time=3) as runner:

            qin.put({'main': Frame(np.zeros((100, 160, 3)), {'meta': {'ts': time()}}, 'BGR')})
            qin.put(False)

            frames = qout.get()

            self.assertTrue(metrics := frames.get('_metrics'))

            keys = set(metrics.data.keys())

            self.assertIn('ts', keys)  # we don't test for correctness, just that they are there
            self.assertIn('fps', keys)
            self.assertIn('cpu', keys)
            self.assertIn('mem', keys)
            self.assertIn('lat_in', keys)
            self.assertIn('lat_out', keys)
            self.assertIn('uptime_count', keys)
            self.assertIn('frame_count', keys)
            self.assertIn('megapx_count', keys)

            self.assertFalse(qout.get())
            self.assertEqual(runner.wait(), [0, 0, 0])


    def test_metrics_dedicated_sender(self):
        with RunnerContext([
            (QueueToFilters, dict(
                outputs = 'ipc://test-Q2F',
                queue   = (qin := mp.Queue()),
            )),
            (Util, dict(
                sources         = 'ipc://test-Q2F',
                outputs         = 'ipc://test-util',
                outputs_metrics = 'ipc://test-util-metrics'
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-util;*',
                queue   = (qout1 := FiltersToQueue.Queue()).child_queue,
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-util-metrics;*',
                queue   = (qout2 := FiltersToQueue.Queue()).child_queue,
            )),
        ], [qin, qout1, qout2], exit_time=3) as runner:

            qin.put({'main': Frame(np.zeros((100, 160, 3)), {'meta': {'ts': time()}}, 'BGR')})
            qin.put(False)

            frames1 = qout1.get()
            frames2 = qout2.get()

            self.assertEqual(list(frames1), ['main'])
            self.assertEqual(list(frames2), ['_metrics'])

            keys = set(frames2['_metrics'].data.keys())

            self.assertIn('ts', keys)  # we don't test for correctness, just that they are there
            self.assertIn('fps', keys)
            self.assertIn('cpu', keys)
            self.assertIn('mem', keys)
            self.assertIn('lat_in', keys)
            self.assertIn('lat_out', keys)
            self.assertIn('uptime_count', keys)
            self.assertIn('frame_count', keys)
            self.assertIn('megapx_count', keys)

            self.assertFalse(qout1.get())
            self.assertFalse(qout2.get())
            self.assertEqual(runner.wait(), [0, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()
