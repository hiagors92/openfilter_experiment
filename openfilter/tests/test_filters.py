#!/usr/bin/env python

import logging
import os
import unittest

from openfilter.filter_runtime.filter import logger as filter_logger
from openfilter.filter_runtime.filters.mqtt_out import MQTTOutConfig, MQTTOut
from openfilter.filter_runtime.filters.recorder import RecorderConfig, Recorder
from openfilter.filter_runtime.filters.rest import RESTConfig, REST
from openfilter.filter_runtime.filters.webvis import WebvisConfig, Webvis

log_level = int(getattr(logging, (os.getenv('LOG_LEVEL') or 'CRITICAL').upper()))

filter_logger.setLevel(log_level)


class TestFilters(unittest.TestCase):
    """Test general stuff of builtin filters, not specific functionality."""

    def test_mqtt_normalize_config(self):
        scfg  = dict(id='mqtt', sources='tcp://localhost:5550', outputs='mqtt://host:1234/base_topic/ ; topic ; topic2/image > topic2_frames')
        dcfg  = MQTTOutConfig({'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': None,
            'src_topic': 'topic', 'src_path': None, 'options': {}},
            {'dst_topic': 'topic2_frames', 'src_topic': 'topic2', 'src_path': 'image', 'options': {}}],
            'base_topic': 'base_topic/', 'broker_host': 'host', 'broker_port': 1234})
        ncfg1 = MQTTOut.normalize_config(scfg)
        ncfg2 = MQTTOut.normalize_config(ncfg1)

        self.assertIsInstance(ncfg1, MQTTOutConfig)
        self.assertIsInstance(ncfg2, MQTTOutConfig)
        self.assertEqual(ncfg1, dcfg)
        self.assertEqual(ncfg1, ncfg2)

        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550',
            broker_host='host', broker_port=1234, base_topic='base_topic/', mappings='topic, topic2/image > topic2_frames')),
            dcfg)

        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': []})
        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='topic')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': None, 'src_topic': 'topic', 'src_path': None, 'options': {}}]})
        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='/image')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': 'frames', 'src_topic': None, 'src_path': 'image', 'options': {}}]})
        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='/data')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': 'data', 'src_topic': None, 'src_path': 'data', 'options': {}}]})
        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='/data/sub')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': 'sub', 'src_topic': None, 'src_path': 'data/sub', 'options': {}}]})
        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='topic/image')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': 'frames', 'src_topic': 'topic', 'src_path': 'image', 'options': {}}]})
        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='topic/image > other')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': 'other', 'src_topic': 'topic', 'src_path': 'image', 'options': {}}]})
        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='topic/image > other ! qos=0 ! retain=true')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': 'other', 'src_topic': 'topic', 'src_path': 'image', 'options': {'qos': 0, 'retain': True}}]})
        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='topic/image')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': 'frames', 'src_topic': 'topic', 'src_path': 'image', 'options': {}}]})
        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='topic/data/sub')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': 'sub', 'src_topic': 'topic', 'src_path': 'data/sub', 'options': {}}]})
        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='topic/data/sub > other')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': 'other', 'src_topic': 'topic', 'src_path': 'data/sub', 'options': {}}]})
        self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings='topic/data/sub/more')),
            {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': 'more', 'src_topic': 'topic', 'src_path': 'data/sub/more', 'options': {}}]})

        # self.assertEqual(MQTTOut.normalize_config(dict(id='mqtt', sources='tcp://localhost:5550', mappings=REPLACE)),
        #     {'id': 'mqtt', 'sources': ['tcp://localhost:5550'], 'mappings': [{'dst_topic': None, 'src_topic': None, 'src_path': None, 'options': {}}]})


    def test_recorder_normalize_config(self):
        scfg  = dict(id='rec', sources='tcp://localhost:5550;main', outputs='file://rec.txt!append', rules='+, -/meta/ts', flush=True)
        dcfg  = RecorderConfig({'id': 'rec', 'sources': ['tcp://localhost:5550;main'], 'outputs': [('file://rec.txt', {'append': True})],
            'rules': ['+', '-/meta/ts'], 'flush': True, '_rules': [(True, None, None), (False, None, ['meta', 'ts'])]})
        ncfg1 = Recorder.normalize_config(scfg)
        ncfg2 = Recorder.normalize_config(ncfg1)

        self.assertIsInstance(ncfg1, RecorderConfig)
        self.assertIsInstance(ncfg2, RecorderConfig)
        self.assertEqual(ncfg1, dcfg)
        self.assertEqual(ncfg1, ncfg2)


    def test_rest_normalize_config(self):
        scfg  = dict(id='rest', sources='http://*:8000/my_base_path/ ; (put|delete|get) test/{param} > rest/zub ; ', outputs='tcp://*')
        dcfg  = RESTConfig({'id': 'rest', 'outputs': ['tcp://*'], 'host': '*', 'port': 8000, 'base_path': 'my_base_path', 'endpoints': [
            {'methods': ['PUT', 'DELETE', 'GET'], 'path': 'test/{param}', 'topic': 'rest/zub'},
            {'path': None, 'topic': 'main', 'methods': ['GET', 'POST']},
        ],'declared_fps': None})

        ncfg1 = REST.normalize_config(scfg)
        ncfg2 = REST.normalize_config(ncfg1)

        self.assertIsInstance(ncfg1, RESTConfig)
        self.assertIsInstance(ncfg2, RESTConfig)
        self.assertEqual(ncfg1, dcfg)
        self.assertEqual(ncfg1, ncfg2)

    def test_webvis_normalize_config(self):
        scfg  = dict(id='webvis', sources='tcp://localhost:5550', outputs='http://0.0.0.0:8000')
        dcfg  = WebvisConfig({'id': 'webvis', 'sources': ['tcp://localhost:5550'], 'host': '0.0.0.0', 'port': 8000})
        ncfg1 = Webvis.normalize_config(scfg)
        ncfg2 = Webvis.normalize_config(ncfg1)

        self.assertIsInstance(ncfg1, WebvisConfig)
        self.assertIsInstance(ncfg2, WebvisConfig)
        self.assertEqual(ncfg1, dcfg)
        self.assertEqual(ncfg1, ncfg2)


if __name__ == '__main__':
    unittest.main()
