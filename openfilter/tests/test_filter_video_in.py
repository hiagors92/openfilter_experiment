#!/usr/bin/env python

import logging
import os
import unittest
from time import sleep

from openfilter.filter_runtime import Filter
from openfilter.filter_runtime.test import FiltersToQueue
from openfilter.filter_runtime.utils import setLogLevelGlobal
from openfilter.filter_runtime.filters.video_in import VideoIn, VideoInConfig

import numpy as np

logger = logging.getLogger(__name__)

log_level = int(getattr(logging, (os.getenv('LOG_LEVEL') or 'CRITICAL').upper()))

setLogLevelGlobal(log_level)

TEST_VIDEO_FNM = 'test_video.mp4'

RED_THEN_GREEN_THEN_BLUE_FRAME_MP4 = (
    b'\x00\x00\x00 ftypisom\x00\x00\x02\x00isomiso2avc1mp41\x00\x00\x00\x08free\x00\x00\x03\xabmdat\x00\x00\x02\xad'
    b'\x06\x05\xff\xff\xa9\xdcE\xe9\xbd\xe6\xd9H\xb7\x96,\xd8 \xd9#\xee\xefx264 - core 163 r3060 5db6aa6 - H.264/MPEG-4'
    b' AVC codec - Copyleft 2003-2021 - http://www.videolan.org/x264.html - options: cabac=1 ref=2 deblock=1:0:0 analys'
    b'e=0x3:0x113 me=hex subme=6 psy=1 psy_rd=1.00:0.00 mixed_ref=1 me_range=16 chroma_me=1 trellis=1 8x8dct=1 cqm=0 de'
    b'adzone=21,11 fast_pskip=1 chroma_qp_offset=4 threads=6 lookahead_threads=1 sliced_threads=0 nr=0 decimate=1 inter'
    b'laced=0 bluray_compat=0 constrained_intra=0 bframes=3 b_pyramid=2 b_adapt=1 b_bias=0 direct=1 weightb=1 open_gop='
    b'0 weightp=1 keyint=250 keyint_min=25 scenecut=40 intra_refresh=0 rc_lookahead=30 rc=crf mbtree=1 crf=18.0 qcomp=0'
    b'.60 qpmin=0 qpmax=69 qpstep=4 ip_ratio=1.40 aq=1:1.00\x00\x80\x00\x00\x007e\x88\x84\x00+\xff\xfe\xf7#\xfc\ni\x83'
    b'\xff\xf0)\x8d\xbd\xff\x02\x9a\xf0g\x7f\xff\xcb\xff\x1a\xb7\\\xabR@d|\x00\x12\xbd\xc8\x02U\x8c\xb3\r\x86\x80\x00'
    b'\x00\x03\x00\x00\x03\x00\rY\x00\x00\x00UA\x9a!i\xe8\x04\x04\x04\x00\x12@\xac\x03\xfd\t\xff\x95@\xf9Oc\xe6\x07\xf6'
    b'Dt\xbe\'\'g~\xaaS\xc1\xeb\xaf\xe0\x10\xd4\x16]|_\xd07\xc3\xb8\xdd\x8bu6\xd0\x91.w\x10j\x1f\xb9\xea\xe8\x00\x00'
    b'\x0b\xfc\x00\x00\x03\x00\xa3\x00\x1f\xe6\xd6\xb1\xa9\xe8\x94v\xb6\xe4d\x00\x1f\x10\x00\x00\x00ZA\x9aB\x13\xd0\r'
    b'\x18\x0f\xe0\x1f\xc0 \x00K\x08O\xff\x90\x1f\xe9\x7f\xfc,&\xa9\xeb\xf2k\xed\xb3<\xfb\xa1\xde\x0f\x1d\x10\xa7\x83'
    b'\xd7_\xc0!\xa8,\xba\xf8\xbf\xa0o\x87q\xbb\x16\xeam\xa1"\\\xee \xd4?s\xd5\xd0\x00\x00\x17\xf8\x00\x00\x03\x01F\x00'
    b'?\xcd\xadcS\xd1(\xedm\xc8\xc8\x00>!\x00\x00\x03?moov\x00\x00\x00lmvhd\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x03\xe8\x00\x00\x00d\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x02\x00\x00\x02itrak\x00\x00\x00\\tkhd\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    b'\x00\x00\x00\x00\x00\x00\x00d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00'
    b'\x00\x00\x01@\x00\x00\x00\xc8\x00\x00\x00\x00\x00$edts\x00\x00\x00\x1celst\x00\x00\x00\x00\x00\x00\x00\x01\x00'
    b'\x00\x00d\x00\x00\x04\x00\x00\x01\x00\x00\x00\x00\x01\xe1mdia\x00\x00\x00 mdhd\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00<\x00\x00\x00\x06\x00U\xc4\x00\x00\x00\x00\x00-hdlr\x00\x00\x00\x00\x00\x00\x00\x00vide'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00VideoHandler\x00\x00\x00\x01\x8cminf\x00\x00\x00\x14vmhd\x00\x00'
    b'\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$dinf\x00\x00\x00\x1cdref\x00\x00\x00\x00\x00\x00\x00\x01\x00'
    b'\x00\x00\x0curl \x00\x00\x00\x01\x00\x00\x01Lstbl\x00\x00\x00\xb0stsd\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'
    b'\xa0avc1\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01@\x00'
    b'\xc8\x00H\x00\x00\x00H\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\xff\xff\x00\x00\x006avcC\x01\xf4'
    b'\x00\r\xff\xe1\x00\x18g\xf4\x00\r\x91\x9b((7\xf10\x80\x00\x00\x03\x00\x80\x00\x00\x1e\x07\x8a\x14\xcb\x01\x00\x07'
    b'h\xea\xe0\x8cD\x84@\xff\xf8\xf8\x00\x00\x00\x00\x14btrt\x00\x00\x00\x00\x00\x01"\xf0\x00\x01"\xf0\x00\x00\x00\x18'
    b'stts\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x02\x00\x00\x00\x00\x14stss\x00\x00\x00\x00\x00\x00'
    b'\x00\x01\x00\x00\x00\x01\x00\x00\x00\x18ctts\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x04\x00\x00'
    b'\x00\x00\x1cstsc\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00 stsz'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x02\xec\x00\x00\x00Y\x00\x00\x00^\x00\x00\x00\x14stco'
    b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x000\x00\x00\x00budta\x00\x00\x00Zmeta\x00\x00\x00\x00\x00\x00\x00!hdlr'
    b'\x00\x00\x00\x00\x00\x00\x00\x00mdirappl\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00-ilst\x00\x00\x00%\xa9too'
    b'\x00\x00\x00\x1ddata\x00\x00\x00\x01\x00\x00\x00\x00Lavf58.76.100')

# BGR is in effect
is_image_very_red   = lambda img: np.mean(img, axis=(0, 1)).dot((0, 0, 255)) >= 0xdfff
is_image_very_green = lambda img: np.mean(img, axis=(0, 1)).dot((0, 255, 0)) >= 0xdfff
is_image_very_blue  = lambda img: np.mean(img, axis=(0, 1)).dot((255, 0, 0)) >= 0xdfff


class TestVideoIn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(TEST_VIDEO_FNM, 'wb') as f:
            f.write(RED_THEN_GREEN_THEN_BLUE_FRAME_MP4)

    @classmethod
    def tearDownClass(cls):
        try:
            os.unlink(TEST_VIDEO_FNM)
        except Exception:
            pass


    def test_normalize_config(self):
        scfg  = dict(id='vidin', sources='webcam://0!bgr, file://SOME_VIDEO_FILE.mp4!sync!loop=3;other, rtsp://RTSP_HOST_ADDRESS:8554/STREAM_NAME!maxsize=640x480;yet_another', outputs='tcp://*')
        dcfg  = VideoInConfig({'id': 'vidin', 'sources': [
            {'source': 'webcam://0', 'topic': 'main', 'options': {'bgr': True}},
            {'source': 'file://SOME_VIDEO_FILE.mp4', 'topic': 'other', 'options': {'sync': True, 'loop': 3}},
            {'source': 'rtsp://RTSP_HOST_ADDRESS:8554/STREAM_NAME', 'topic': 'yet_another', 'options': {'maxsize': '640x480'}}],
            'outputs': ['tcp://*']})
        ncfg1 = VideoIn.normalize_config(scfg)
        ncfg2 = VideoIn.normalize_config(ncfg1)

        self.assertIsInstance(ncfg1, VideoInConfig)
        self.assertIsInstance(ncfg2, VideoInConfig)
        self.assertEqual(ncfg1, dcfg)
        self.assertEqual(ncfg1, ncfg2)


    def test_read(self):
        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync',  # '!sync' to make it step one frame at a time as fast as possible
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertTrue(is_image_very_red(image := queue.get()['main'].image))
            self.assertFalse(is_image_very_green(image))  # ensure the failing case to validate the successful
            self.assertFalse(is_image_very_blue(image))
            self.assertTrue(is_image_very_green(image := queue.get()['main'].image))
            self.assertFalse(is_image_very_red(image))
            self.assertFalse(is_image_very_blue(image))
            self.assertTrue(is_image_very_blue(image := queue.get()['main'].image))
            self.assertFalse(is_image_very_red(image))
            self.assertFalse(is_image_very_green(image))
            self.assertFalse(queue.get())

        finally:
            runner.stop()
            queue.close()


    def test_bgr(self):
        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!bgr',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertEqual((frame := queue.get()['main']).format, 'BGR')
            self.assertTrue(is_image_very_red(frame.image))

        finally:
            runner.stop()
            queue.close()

        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!no-bgr',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertEqual((frame := queue.get()['main']).format, 'RGB')
            self.assertTrue(is_image_very_blue(frame.image))  # because is backwards of "normal"

        finally:
            runner.stop()
            queue.close()


    def test_sync(self):
        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertTrue(is_image_very_red(queue.get()['main'].image))
            self.assertTrue(is_image_very_green(queue.get()['main'].image))

            sleep(1)  # wait enough time to ensure the video reading was paused

            self.assertTrue(is_image_very_blue(queue.get()['main'].image))
            self.assertFalse(queue.get())

        finally:
            runner.stop()
            queue.close()


    def test_loop(self):
        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!loop=3',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertTrue(is_image_very_red(queue.get()['main'].image))
            self.assertTrue(is_image_very_green(queue.get()['main'].image))
            self.assertTrue(is_image_very_blue(queue.get()['main'].image))
            self.assertTrue(is_image_very_red(queue.get()['main'].image))
            self.assertTrue(is_image_very_green(queue.get()['main'].image))
            self.assertTrue(is_image_very_blue(queue.get()['main'].image))
            self.assertTrue(is_image_very_red(queue.get()['main'].image))
            self.assertTrue(is_image_very_green(queue.get()['main'].image))
            self.assertTrue(is_image_very_blue(queue.get()['main'].image))
            self.assertFalse(queue.get())

        finally:
            runner.stop()
            queue.close()


    def test_maxfps(self):  # INCOMPLETE, doesn't test non-sync maxfps
        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!maxfps=2',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            frm0 = queue.get()['main']
            frm1 = queue.get()['main']
            frm2 = queue.get()['main']

            self.assertFalse(queue.get())
            self.assertTrue(abs(frm2.data['meta']['ts'] - frm0.data['meta']['ts']) >= 0.8)  # this check instead of more accurate because of iaccuracies in VM

        finally:
            runner.stop()
            queue.close()


    def test_resize(self):
        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!resize=160x100',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertEqual(queue.get()['main'].shape, (100, 160, 3))

        finally:
            runner.stop()
            queue.close()

        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!resize=160x80',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertEqual(queue.get()['main'].shape, (80, 128, 3))

        finally:
            runner.stop()
            queue.close()

        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!resize=160+80',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertEqual(queue.get()['main'].shape, (80, 160, 3))

        finally:
            runner.stop()
            queue.close()

        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!resize=640x400',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertEqual(queue.get()['main'].shape, (400, 640, 3))

        finally:
            runner.stop()
            queue.close()


    def test_maxsize(self):
        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!maxsize=160x100',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertEqual(queue.get()['main'].shape, (100, 160, 3))

        finally:
            runner.stop()
            queue.close()

        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!maxsize=160x80',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertEqual(queue.get()['main'].shape, (80, 128, 3))

        finally:
            runner.stop()
            queue.close()

        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!maxsize=160+80',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertEqual(queue.get()['main'].shape, (80, 160, 3))

        finally:
            runner.stop()
            queue.close()

        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}!sync!maxsize=640x400',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertEqual(queue.get()['main'].shape, (200, 320, 3))

        finally:
            runner.stop()
            queue.close()


    def test_multiple_videos(self):
        runner = Filter.Runner([
            (VideoIn, dict(
                sources = \
                    f'file://{TEST_VIDEO_FNM}!sync;vid0, '
                    f'file://{TEST_VIDEO_FNM}!sync;vid1, '
                    f'file://{TEST_VIDEO_FNM}!sync!maxsize=160x100;vid2',
                outputs = 'ipc://test-VideoIn',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            frm0 = queue.get()
            frm1 = queue.get()
            frm2 = queue.get()

            # TODO: Below assertFalse() is commented out because sometimes the clean exit message just disappears in
            # transit. I've tracked it down to being sent, and the receiver is waiting for messages, and a multisecond
            # LINGER on the sender after send should make sure that it goes out on the socket, but the receiver never
            # gets it despite being in a receive state for everything with the poller having the only upstream connected
            # socket in its list of polling. The initial topic informative message for the previous set of frames gets
            # there but the exit message just disappears while the polling keeps going on! It looks like it is never
            # actually sent from upstream despite a large amount of time being allowed for this to happen.

            # self.assertFalse(queue.get())

            self.assertEqual(set(frm0), keys := set(['vid0', 'vid1', 'vid2']))
            self.assertEqual(set(frm1), keys)
            self.assertEqual(set(frm2), keys)

            self.assertEqual(frm0['vid0'].shape, (200, 320, 3))
            self.assertEqual(frm0['vid1'].shape, (200, 320, 3))
            self.assertEqual(frm0['vid2'].shape, (100, 160, 3))
            self.assertEqual(frm1['vid0'].shape, (200, 320, 3))
            self.assertEqual(frm1['vid1'].shape, (200, 320, 3))
            self.assertEqual(frm1['vid2'].shape, (100, 160, 3))
            self.assertEqual(frm2['vid0'].shape, (200, 320, 3))
            self.assertEqual(frm2['vid1'].shape, (200, 320, 3))
            self.assertEqual(frm2['vid2'].shape, (100, 160, 3))

        finally:
            runner.stop()
            queue.close()


    def test_config_params(self):
        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}',
                outputs = 'ipc://test-VideoIn',
                bgr     = False,
                sync    = True,
                loop    = 2,
                resize  = '160x100',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            self.assertTrue(is_image_very_blue((frame := queue.get()['main']).image))  # red/blue check flipped because bgr=False
            self.assertEqual(frame.format, 'RGB')
            self.assertEqual(frame.shape, (100, 160, 3))
            self.assertTrue(is_image_very_green(queue.get()['main'].image))
            self.assertTrue(is_image_very_red(queue.get()['main'].image))
            self.assertTrue(is_image_very_blue(queue.get()['main'].image))
            self.assertTrue(is_image_very_green(queue.get()['main'].image))
            self.assertTrue(is_image_very_red(queue.get()['main'].image))
            self.assertFalse(queue.get())

        finally:
            runner.stop()
            queue.close()

        runner = Filter.Runner([
            (VideoIn, dict(
                sources = f'file://{TEST_VIDEO_FNM}',
                outputs = 'ipc://test-VideoIn',
                bgr     = True,
                sync    = True,
                loop    = 1,
                maxfps  = 2,
                maxsize = '160x80',
            )),
            (FiltersToQueue, dict(
                sources = 'ipc://test-VideoIn',
                queue   = (queue := FiltersToQueue.Queue()).child_queue,
            )),
        ], exit_time=3)

        try:
            frm0 = queue.get()['main']
            frm1 = queue.get()['main']
            frm2 = queue.get()['main']

            self.assertTrue(is_image_very_red((frame := frm0).image))
            self.assertEqual(frame.format, 'BGR')
            self.assertEqual(frame.shape, (80, 128, 3))
            self.assertTrue(is_image_very_green(frm1.image))
            self.assertTrue(is_image_very_blue(frm2.image))
            self.assertFalse(queue.get())
            self.assertTrue(frm2.data['meta']['ts'] - frm0.data['meta']['ts'] >= 0.8)  # this check instead of more accurate because of iaccuracies in VM

        finally:
            runner.stop()
            queue.close()


if __name__ == '__main__':
    unittest.main()
