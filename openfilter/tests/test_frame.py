#!/usr/bin/env python

# NOTE: Don't really need THIS many redundant tests, but just went adding as developed so left them in, harmless.

import unittest

import cv2
import numpy as np
import pickle
from numpy import array_equal as aeq

from openfilter.filter_runtime import Frame


class TestFrame(unittest.TestCase):
    def test_old(self):
        image_rgb        = np.array([[[1,2,3], [4,5,6]], [[7,8,9],[9,8,7]], [[1,0,0], [2,0,0]]], np.uint8)
        image_bgr        = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        image_jpg_rgb    = cv2.imencode('.jpg', image_rgb)[1]
        image_jpg_bgr    = cv2.imencode('.jpg', image_bgr)[1]
        frm_raw_rgb_rw   = Frame(image_rgb, {}, 'RGB')
        frm_raw_bgr_rw   = Frame(image_bgr, {}, 'BGR')
        frm_raw_rgb_ro   = Frame(image_rgb, {}, 'RGB').ro
        frm_raw_bgr_ro   = Frame(image_bgr, {}, 'BGR').ro
        frm_jpg_rgb      = Frame.from_jpg(image_jpg_rgb, {}, 3, 2, 'RGB')
        frm_jpg_bgr      = Frame.from_jpg(image_jpg_bgr, {}, 3, 2, 'BGR')
        frm_plus_jpg_rgb = Frame.from_jpg(image_jpg_rgb, {}, 3, 2, 'RGB')
        frm_plus_jpg_bgr = Frame.from_jpg(image_jpg_bgr, {}, 3, 2, 'BGR')

        frm_plus_jpg_rgb.image  # trigger decode
        frm_plus_jpg_bgr.image

        self.assertTrue(Frame({}).image is None)
        self.assertTrue(Frame(d := {}).data is d)
        self.assertTrue(Frame(None, {}).image is None)
        self.assertTrue(Frame(None, d := {}).data is d)

        self.assertFalse(frm_jpg_rgb.jpg == frm_jpg_bgr.jpg)
        self.assertTrue(frm_jpg_rgb.jpg == frm_plus_jpg_rgb.jpg)
        self.assertFalse(frm_jpg_rgb.jpg == frm_plus_jpg_bgr.jpg)

        self.assertTrue(aeq(image_rgb, frm_raw_rgb_rw.copy().image))
        self.assertTrue(aeq(image_rgb, frm_raw_rgb_ro.copy().image))
        self.assertTrue(aeq(image_bgr, frm_raw_bgr_rw.copy().image))
        self.assertTrue(aeq(image_bgr, frm_raw_bgr_ro.copy().image))
        self.assertTrue(aeq(image_jpg_rgb, frm_jpg_rgb.copy().jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_jpg_bgr.copy().jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_rgb_rw.copy().jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_rgb_ro.copy().jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_bgr_rw.copy().jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_bgr_ro.copy().jpg))

        self.assertTrue(aeq(image_rgb, frm_raw_rgb_rw.copy().rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_rgb_rw.copy().rw.image))
        self.assertTrue(aeq(image_rgb, frm_raw_rgb_rw.copy().ro.image))
        self.assertTrue(aeq(image_rgb, frm_raw_rgb_rw.copy().rgb.rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_rgb_rw.copy().rgb.rw.image))
        self.assertTrue(aeq(image_rgb, frm_raw_rgb_rw.copy().rgb.ro.image))
        self.assertTrue(aeq(image_rgb, frm_raw_rgb_rw.copy().rgb.rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_rgb_rw.copy().rw.rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_rgb_rw.copy().ro.rgb.image))

        self.assertTrue(aeq(image_bgr, frm_raw_rgb_rw.copy().rgb.bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_rgb_rw.copy().rw.bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_rgb_rw.copy().ro.bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_rgb_rw.copy().rgb.rgb.bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_rgb_rw.copy().rgb.rw.bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_rgb_rw.copy().rgb.ro.bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_rgb_rw.copy().rgb.rgb.bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_rgb_rw.copy().rw.rgb.bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_rgb_rw.copy().ro.rgb.bgr.image))

        self.assertTrue(aeq(image_bgr, frm_raw_bgr_rw.copy().bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_bgr_rw.copy().rw.image))
        self.assertTrue(aeq(image_bgr, frm_raw_bgr_rw.copy().ro.image))
        self.assertTrue(aeq(image_bgr, frm_raw_bgr_rw.copy().bgr.bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_bgr_rw.copy().bgr.rw.image))
        self.assertTrue(aeq(image_bgr, frm_raw_bgr_rw.copy().bgr.ro.image))
        self.assertTrue(aeq(image_bgr, frm_raw_bgr_rw.copy().bgr.bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_bgr_rw.copy().rw.bgr.image))
        self.assertTrue(aeq(image_bgr, frm_raw_bgr_rw.copy().ro.bgr.image))

        self.assertTrue(aeq(image_rgb, frm_raw_bgr_rw.copy().bgr.rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_bgr_rw.copy().rw.rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_bgr_rw.copy().ro.rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_bgr_rw.copy().bgr.bgr.rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_bgr_rw.copy().bgr.rw.rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_bgr_rw.copy().bgr.ro.rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_bgr_rw.copy().bgr.rgb.rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_bgr_rw.copy().rw.bgr.rgb.image))
        self.assertTrue(aeq(image_rgb, frm_raw_bgr_rw.copy().ro.bgr.rgb.image))

        self.assertTrue(aeq(image_rgb, frm_raw_bgr_rw.copy().ro.rgb.rw.bgr.ro.rgb.rw.image))
        self.assertTrue(aeq(image_bgr, frm_raw_rgb_rw.copy().ro.bgr.rw.rgb.ro.bgr.rw.image))

        self.assertTrue(aeq(image_jpg_rgb, frm_raw_rgb_rw.copy().rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_rgb_rw.copy().rw.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_rgb_rw.copy().ro.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_rgb_rw.copy().rgb.rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_rgb_rw.copy().rgb.rw.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_rgb_rw.copy().rgb.ro.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_rgb_rw.copy().rgb.rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_rgb_rw.copy().rw.rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_rgb_rw.copy().ro.rgb.jpg))

        self.assertTrue(aeq(image_jpg_bgr, frm_raw_rgb_rw.copy().rgb.bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_rgb_rw.copy().rw.bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_rgb_rw.copy().ro.bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_rgb_rw.copy().rgb.rgb.bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_rgb_rw.copy().rgb.rw.bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_rgb_rw.copy().rgb.ro.bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_rgb_rw.copy().rgb.rgb.bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_rgb_rw.copy().rw.rgb.bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_rgb_rw.copy().ro.rgb.bgr.jpg))

        self.assertTrue(aeq(image_jpg_bgr, frm_raw_bgr_rw.copy().bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_bgr_rw.copy().rw.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_bgr_rw.copy().ro.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_bgr_rw.copy().bgr.bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_bgr_rw.copy().bgr.rw.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_bgr_rw.copy().bgr.ro.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_bgr_rw.copy().bgr.bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_bgr_rw.copy().rw.bgr.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_bgr_rw.copy().ro.bgr.jpg))

        self.assertTrue(aeq(image_jpg_rgb, frm_raw_bgr_rw.copy().bgr.rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_bgr_rw.copy().rw.rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_bgr_rw.copy().ro.rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_bgr_rw.copy().bgr.bgr.rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_bgr_rw.copy().bgr.rw.rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_bgr_rw.copy().bgr.ro.rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_bgr_rw.copy().bgr.rgb.rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_bgr_rw.copy().rw.bgr.rgb.jpg))
        self.assertTrue(aeq(image_jpg_rgb, frm_raw_bgr_rw.copy().ro.bgr.rgb.jpg))

        self.assertTrue(aeq(image_jpg_rgb, frm_raw_bgr_rw.copy().ro.rgb.rw.bgr.ro.rgb.rw.jpg))
        self.assertTrue(aeq(image_jpg_bgr, frm_raw_rgb_rw.copy().ro.bgr.rw.rgb.ro.bgr.rw.jpg))


    def test_self(self):
        image_rgb        = np.array([[[1,2,3], [4,5,6]], [[7,8,9],[9,8,7]], [[1,0,0], [2,0,0]]], np.uint8)
        image_bgr        = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        image_jpg        = cv2.imencode('.jpg', image_bgr)[1]
        frm_raw_rgb_rw   = Frame(image_rgb, {}, 'RGB')
        frm_raw_bgr_rw   = Frame(image_bgr, {}, 'BGR')
        frm_raw_rgb_ro   = Frame(image_rgb, {}, 'RGB').ro
        frm_raw_bgr_ro   = Frame(image_bgr, {}, 'BGR').ro
        frm_jpg_rgb      = Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB')
        frm_jpg_bgr      = Frame.from_jpg(image_jpg, {}, 3, 2, 'BGR')
        frm_plus_jpg_rgb = Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB').ro
        frm_plus_jpg_bgr = Frame.from_jpg(image_jpg, {}, 3, 2, 'BGR').ro

        frm_plus_jpg_rgb.image  # trigger decode
        frm_plus_jpg_bgr.image

        self.assertTrue(frm_raw_rgb_rw is frm_raw_rgb_rw.rw)
        self.assertTrue(frm_raw_rgb_rw is not frm_raw_rgb_rw.ro)
        self.assertTrue(frm_raw_rgb_ro is not frm_raw_rgb_ro.rw)
        self.assertTrue(frm_raw_rgb_ro is frm_raw_rgb_ro.ro)

        self.assertTrue(frm_raw_rgb_rw is frm_raw_rgb_rw.rgb)
        self.assertTrue(frm_raw_rgb_rw is not frm_raw_rgb_rw.bgr)
        self.assertTrue(frm_raw_rgb_rw is frm_raw_rgb_rw.rw_rgb)
        self.assertTrue(frm_raw_rgb_rw is not frm_raw_rgb_rw.rw_bgr)
        self.assertTrue(frm_raw_rgb_rw is not frm_raw_rgb_rw.ro_rgb)
        self.assertTrue(frm_raw_rgb_rw is not frm_raw_rgb_rw.ro_bgr)

        self.assertTrue(frm_raw_rgb_ro is frm_raw_rgb_ro.rgb)
        self.assertTrue(frm_raw_rgb_ro is not frm_raw_rgb_ro.bgr)
        self.assertTrue(frm_raw_rgb_ro is not frm_raw_rgb_ro.rw_rgb)
        self.assertTrue(frm_raw_rgb_ro is not frm_raw_rgb_ro.rw_bgr)
        self.assertTrue(frm_raw_rgb_ro is frm_raw_rgb_ro.ro_rgb)
        self.assertTrue(frm_raw_rgb_ro is not frm_raw_rgb_ro.ro_bgr)

        self.assertTrue(frm_raw_bgr_rw is not frm_raw_bgr_rw.rgb)
        self.assertTrue(frm_raw_bgr_rw is frm_raw_bgr_rw.bgr)
        self.assertTrue(frm_raw_bgr_rw is not frm_raw_bgr_rw.rw_rgb)
        self.assertTrue(frm_raw_bgr_rw is frm_raw_bgr_rw.rw_bgr)
        self.assertTrue(frm_raw_bgr_rw is not frm_raw_bgr_rw.ro_rgb)
        self.assertTrue(frm_raw_bgr_rw is not frm_raw_bgr_rw.ro_bgr)

        self.assertTrue(frm_raw_bgr_ro is not frm_raw_bgr_ro.rgb)
        self.assertTrue(frm_raw_bgr_ro is frm_raw_bgr_ro.bgr)
        self.assertTrue(frm_raw_bgr_ro is not frm_raw_bgr_ro.rw_rgb)
        self.assertTrue(frm_raw_bgr_ro is not frm_raw_bgr_ro.rw_bgr)
        self.assertTrue(frm_raw_bgr_ro is not frm_raw_bgr_ro.ro_rgb)
        self.assertTrue(frm_raw_bgr_ro is frm_raw_bgr_ro.ro_bgr)

        self.assertTrue(frm_jpg_rgb is not frm_jpg_rgb.rw)
        self.assertTrue(frm_jpg_rgb is frm_jpg_rgb.ro)
        self.assertTrue(frm_jpg_rgb is frm_jpg_rgb.rgb)
        self.assertTrue(frm_jpg_rgb is not frm_jpg_rgb.bgr)
        self.assertTrue(frm_jpg_rgb is not frm_jpg_rgb.rw_rgb)
        self.assertTrue(frm_jpg_rgb is not frm_jpg_rgb.rw_bgr)
        self.assertTrue(frm_jpg_rgb is frm_jpg_rgb.ro_rgb)
        self.assertTrue(frm_jpg_rgb is not frm_jpg_rgb.ro_bgr)

        self.assertTrue(frm_jpg_bgr is not frm_jpg_bgr.rw)
        self.assertTrue(frm_jpg_bgr is frm_jpg_bgr.ro)
        self.assertTrue(frm_jpg_bgr is not frm_jpg_bgr.rgb)
        self.assertTrue(frm_jpg_bgr is frm_jpg_bgr.bgr)
        self.assertTrue(frm_jpg_bgr is not frm_jpg_bgr.rw_rgb)
        self.assertTrue(frm_jpg_bgr is not frm_jpg_bgr.rw_bgr)
        self.assertTrue(frm_jpg_bgr is not frm_jpg_bgr.ro_rgb)
        self.assertTrue(frm_jpg_bgr is frm_jpg_bgr.ro_bgr)


    def test_cache(self):
        image_rgb = np.array([[[1,2,3], [4,5,6]], [[7,8,9],[9,8,7]], [[1,0,0], [2,0,0]]], np.uint8)
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        self.assertTrue((frm_raw_rgb_ro := Frame(image_rgb, {}, 'BGR').ro).bgr is frm_raw_rgb_ro.bgr)
        self.assertTrue((frm_raw_rgb_ro := Frame(image_rgb, {}, 'BGR').ro).bgr is frm_raw_rgb_ro.ro_bgr)
        self.assertTrue((frm_raw_rgb_ro := Frame(image_rgb, {}, 'BGR').ro).ro_bgr is frm_raw_rgb_ro.bgr)
        self.assertTrue((frm_raw_rgb_ro := Frame(image_rgb, {}, 'BGR').ro).ro_bgr is frm_raw_rgb_ro.ro_bgr)

        self.assertTrue((frm_raw_bgr_ro := Frame(image_bgr, {}, 'BGR').ro).rgb is frm_raw_bgr_ro.rgb)
        self.assertTrue((frm_raw_bgr_ro := Frame(image_bgr, {}, 'BGR').ro).rgb is frm_raw_bgr_ro.ro_rgb)
        self.assertTrue((frm_raw_bgr_ro := Frame(image_bgr, {}, 'BGR').ro).ro_rgb is frm_raw_bgr_ro.rgb)
        self.assertTrue((frm_raw_bgr_ro := Frame(image_bgr, {}, 'BGR').ro).ro_rgb is frm_raw_bgr_ro.ro_rgb)


    def test_writability(self):
        image_rgb = np.array([[[1,2,3], [4,5,6]], [[7,8,9],[9,8,7]], [[1,0,0], [2,0,0]]], np.uint8)
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        image_jpg = cv2.imencode('.jpg', image_bgr)[1]
        is_rw     = lambda f: isinstance(f.image, np.ndarray) and f.image.flags.writeable
        is_ro     = lambda f: isinstance(f.image, np.ndarray) and not f.image.flags.writeable

        self.assertTrue(is_rw(Frame(image_rgb, format='BGR')))
        self.assertTrue(Frame(image_rgb, format='BGR').is_rw)
        self.assertTrue(is_ro(Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB')))
        self.assertTrue(Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB').is_ro)

        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').rw))
        self.assertTrue(Frame(image_rgb, format='BGR').rw.is_rw)
        self.assertTrue(is_rw(Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB').rw))
        self.assertTrue(Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB').rw.is_rw)

        self.assertTrue(is_ro(Frame(image_rgb, format='BGR').ro))
        self.assertTrue(Frame(image_rgb, format='BGR').ro.is_ro)
        self.assertTrue(is_ro(Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB').ro))
        self.assertTrue(Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB').ro.is_ro)

        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').rgb))
        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').bgr))

        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').rw.rgb))
        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').rgb.rw))
        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').rw.rgb.rw))
        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').rw.bgr))
        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').bgr.rw))
        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').rw.bgr.rw))

        self.assertTrue(is_ro(Frame(image_rgb, format='BGR').ro.rgb))
        self.assertTrue(is_ro(Frame(image_rgb, format='BGR').rgb.ro))
        self.assertTrue(is_ro(Frame(image_rgb, format='BGR').ro.rgb.ro))
        self.assertTrue(is_ro(Frame(image_rgb, format='BGR').ro.bgr))
        self.assertTrue(is_ro(Frame(image_rgb, format='BGR').bgr.ro))
        self.assertTrue(is_ro(Frame(image_rgb, format='BGR').ro.bgr.ro))

        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').rw_rgb))
        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').ro.rw_rgb))
        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').rw_bgr))
        self.assertTrue(is_rw(Frame(image_rgb, format='BGR').ro.rw_bgr))
        self.assertTrue(is_rw(Frame(image_bgr, {}, 'BGR').rw_rgb))
        self.assertTrue(is_rw(Frame(image_bgr, {}, 'BGR').ro.rw_rgb))
        self.assertTrue(is_rw(Frame(image_bgr, {}, 'BGR').rw_bgr))
        self.assertTrue(is_rw(Frame(image_bgr, {}, 'BGR').ro.rw_bgr))

        self.assertTrue(is_ro(Frame(image_rgb, format='BGR').ro_rgb))
        self.assertTrue(is_ro(Frame(image_rgb, format='BGR').rw.ro_rgb))
        self.assertTrue(is_ro(Frame(image_rgb, format='BGR').ro_bgr))
        self.assertTrue(is_ro(Frame(image_rgb, format='BGR').rw.ro_bgr))
        self.assertTrue(is_ro(Frame(image_bgr, {}, 'BGR').ro_rgb))
        self.assertTrue(is_ro(Frame(image_bgr, {}, 'BGR').rw.ro_rgb))
        self.assertTrue(is_ro(Frame(image_bgr, {}, 'BGR').ro_bgr))
        self.assertTrue(is_ro(Frame(image_bgr, {}, 'BGR').rw.ro_bgr))


    def test_formats(self):
        image_rgb        = np.array([[[1,2,3], [4,5,6]], [[7,8,9],[9,8,7]], [[1,0,0], [2,0,0]]], np.uint8)
        image_bgr        = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        image_jpg        = cv2.imencode('.jpg', image_bgr)[1]
        frm_raw_rgb_rw   = Frame(image_rgb, {}, 'RGB')
        frm_raw_bgr_rw   = Frame(image_bgr, {}, 'BGR')
        frm_raw_rgb_ro   = Frame(image_rgb, {}, 'RGB').ro
        frm_raw_bgr_ro   = Frame(image_bgr, {}, 'BGR').ro
        frm_jpg_rgb      = Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB')
        frm_jpg_bgr      = Frame.from_jpg(image_jpg, {}, 3, 2, 'BGR')
        frm_plus_jpg_rgb = Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB')
        frm_plus_jpg_bgr = Frame.from_jpg(image_jpg, {}, 3, 2, 'BGR')

        frm_plus_jpg_rgb.image  # trigger decode
        frm_plus_jpg_bgr.image

        self.assertEqual(str(frm_raw_rgb_rw), 'Frame(2x3xRGB)')
        self.assertEqual(str(frm_raw_bgr_rw), 'Frame(2x3xBGR)')
        self.assertEqual(str(frm_raw_rgb_ro), 'Frame(2x3xRGB-ro)')
        self.assertEqual(str(frm_raw_bgr_ro), 'Frame(2x3xBGR-ro)')
        self.assertEqual(str(frm_jpg_rgb), 'Frame(2x3xRGB-jpg)')
        self.assertEqual(str(frm_jpg_bgr), 'Frame(2x3xBGR-jpg)')
        self.assertEqual(str(frm_plus_jpg_rgb), 'Frame(2x3xRGB+jpg)')
        self.assertEqual(str(frm_plus_jpg_bgr), 'Frame(2x3xBGR+jpg)')

        self.assertEqual(str(frm_jpg_rgb.rgb), 'Frame(2x3xRGB-jpg)')
        self.assertEqual(str(frm_jpg_bgr.bgr), 'Frame(2x3xBGR-jpg)')
        self.assertEqual(str(frm_plus_jpg_rgb.rgb), 'Frame(2x3xRGB+jpg)')
        self.assertEqual(str(frm_plus_jpg_bgr.bgr), 'Frame(2x3xBGR+jpg)')

        self.assertEqual(str(frm_jpg_rgb.copy().bgr), 'Frame(2x3xBGR-ro)')
        self.assertEqual(str(frm_jpg_bgr.copy().rgb), 'Frame(2x3xRGB-ro)')
        self.assertEqual(str(frm_plus_jpg_rgb.bgr), 'Frame(2x3xBGR-ro)')
        self.assertEqual(str(frm_plus_jpg_bgr.rgb), 'Frame(2x3xRGB-ro)')

        self.assertEqual(str(frm_jpg_rgb.copy().bgr.ro), 'Frame(2x3xBGR-ro)')
        self.assertEqual(str(frm_jpg_bgr.copy().rgb.ro), 'Frame(2x3xRGB-ro)')
        self.assertEqual(str(frm_plus_jpg_rgb.bgr.ro), 'Frame(2x3xBGR-ro)')
        self.assertEqual(str(frm_plus_jpg_bgr.rgb.ro), 'Frame(2x3xRGB-ro)')

        self.assertEqual(str(frm_jpg_rgb.copy().bgr.rw), 'Frame(2x3xBGR)')
        self.assertEqual(str(frm_jpg_bgr.copy().rgb.rw), 'Frame(2x3xRGB)')
        self.assertEqual(str(frm_plus_jpg_rgb.bgr.rw), 'Frame(2x3xBGR)')
        self.assertEqual(str(frm_plus_jpg_bgr.rgb.rw), 'Frame(2x3xRGB)')

        self.assertEqual(str(frm_raw_rgb_rw.ro), 'Frame(2x3xRGB-ro)')
        self.assertEqual(str(frm_raw_bgr_rw.ro), 'Frame(2x3xBGR-ro)')
        self.assertEqual(str(frm_raw_rgb_ro.rw), 'Frame(2x3xRGB)')
        self.assertEqual(str(frm_raw_bgr_ro.rw), 'Frame(2x3xBGR)')

        self.assertEqual(str(frm_raw_rgb_rw.ro.bgr), 'Frame(2x3xBGR-ro)')
        self.assertEqual(str(frm_raw_bgr_rw.ro.rgb), 'Frame(2x3xRGB-ro)')
        self.assertEqual(str(frm_raw_rgb_ro.rw.bgr), 'Frame(2x3xBGR)')
        self.assertEqual(str(frm_raw_bgr_ro.rw.rgb), 'Frame(2x3xRGB)')

        self.assertEqual(str(frm_jpg_rgb.ro_rgb), 'Frame(2x3xRGB-jpg)')
        self.assertEqual(str(frm_jpg_rgb.copy().ro_bgr), 'Frame(2x3xBGR-ro)')
        self.assertEqual(str(frm_jpg_rgb.copy().rw_rgb), 'Frame(2x3xRGB)')
        self.assertEqual(str(frm_jpg_rgb.copy().rw_bgr), 'Frame(2x3xBGR)')
        self.assertEqual(str(frm_jpg_bgr.copy().ro_rgb), 'Frame(2x3xRGB-ro)')
        self.assertEqual(str(frm_jpg_bgr.ro_bgr), 'Frame(2x3xBGR-jpg)')
        self.assertEqual(str(frm_jpg_bgr.copy().rw_rgb), 'Frame(2x3xRGB)')
        self.assertEqual(str(frm_jpg_bgr.copy().rw_bgr), 'Frame(2x3xBGR)')

        self.assertRaises(ValueError, lambda: Frame(image_rgb, {}, 'INVALID FORMAT!!!'))
        self.assertRaises(ValueError, lambda: Frame.from_jpg(image_jpg, {}, 3, 2, 'INVALID FORMAT!!!'))


    def test_gray(self):
        image_gray        = np.array([[0, 255], [63, 127], [191, 255]], np.uint8)
        image_3ch         = np.array([[[0,0,0], [255,255,255]], [[63,63,63],[127,127,127]], [[191,191,191], [255,255,255]]], np.uint8)
        image_jpg         = cv2.imencode('.jpg', image_gray)[1]
        frm_raw_gray_rw   = Frame(image_gray, {})
        frm_raw_gray_ro   = Frame(image_gray, {}).ro
        frm_jpg_gray      = Frame.from_jpg(image_jpg, {}, 3, 2, 'GRAY')
        frm_plus_jpg_gray = Frame.from_jpg(image_jpg, {}, 3, 2, 'GRAY')

        frm_plus_jpg_gray.image  # trigger decode

        self.assertEqual(str(frm_raw_gray_rw), 'Frame(2x3xGRAY)')
        self.assertEqual(str(frm_raw_gray_ro), 'Frame(2x3xGRAY-ro)')
        self.assertEqual(str(frm_jpg_gray), 'Frame(2x3xGRAY-jpg)')
        self.assertEqual(str(frm_plus_jpg_gray), 'Frame(2x3xGRAY+jpg)')

        self.assertTrue(aeq(image_gray, frm_raw_gray_rw.copy().rw.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_rw.copy().ro.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_rw.copy().rgb.gray.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_rw.copy().bgr.gray.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_rw.copy().rw_rgb.gray.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_rw.copy().ro_rgb.gray.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_rw.copy().rw_bgr.gray.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_rw.copy().ro_bgr.gray.image))

        self.assertTrue(aeq(image_gray, frm_raw_gray_ro.copy().rw.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_ro.copy().ro.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_ro.copy().rgb.gray.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_ro.copy().bgr.gray.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_ro.copy().rw_rgb.gray.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_ro.copy().ro_rgb.gray.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_ro.copy().rw_bgr.gray.image))
        self.assertTrue(aeq(image_gray, frm_raw_gray_ro.copy().ro_bgr.gray.image))

        self.assertTrue(aeq(image_3ch, frm_raw_gray_rw.copy().rgb.image))
        self.assertTrue(aeq(image_3ch, frm_raw_gray_rw.copy().bgr.image))
        self.assertTrue(aeq(image_3ch, frm_raw_gray_rw.copy().rw_rgb.image))
        self.assertTrue(aeq(image_3ch, frm_raw_gray_rw.copy().ro_rgb.image))
        self.assertTrue(aeq(image_3ch, frm_raw_gray_rw.copy().rw_bgr.image))
        self.assertTrue(aeq(image_3ch, frm_raw_gray_rw.copy().ro_bgr.image))

        self.assertTrue(aeq(image_3ch, frm_raw_gray_ro.copy().rgb.image))
        self.assertTrue(aeq(image_3ch, frm_raw_gray_ro.copy().bgr.image))
        self.assertTrue(aeq(image_3ch, frm_raw_gray_ro.copy().rw_rgb.image))
        self.assertTrue(aeq(image_3ch, frm_raw_gray_ro.copy().ro_rgb.image))
        self.assertTrue(aeq(image_3ch, frm_raw_gray_ro.copy().rw_bgr.image))
        self.assertTrue(aeq(image_3ch, frm_raw_gray_ro.copy().ro_bgr.image))

        self.assertTrue((f := frm_raw_gray_rw.ro.rgb).gray is f.gray)
        self.assertTrue((f := frm_raw_gray_rw.ro.bgr).gray is f.gray)
        self.assertTrue((f := frm_raw_gray_rw.ro_rgb).gray is f.gray)
        self.assertTrue((f := frm_raw_gray_rw.ro_bgr).gray is f.gray)
        self.assertTrue((f := frm_raw_gray_rw.ro.ro_rgb).gray is f.gray)
        self.assertTrue((f := frm_raw_gray_rw.ro.ro_bgr).gray is f.gray)

        self.assertTrue(frm_raw_gray_ro is frm_raw_gray_ro.ro)
        self.assertTrue(frm_raw_gray_rw.jpg is not frm_raw_gray_rw.jpg)
        self.assertTrue(frm_raw_gray_ro.jpg is frm_raw_gray_ro.jpg)

        self.assertTrue(aeq(image_jpg, frm_raw_gray_rw.jpg))
        self.assertTrue(aeq(image_jpg, frm_raw_gray_ro.jpg))


    def test_convert(self):
        image_rgb         = np.array([[[1,2,3], [4,5,6]], [[7,8,9],[9,8,7]], [[1,0,0], [2,0,0]]], np.uint8)
        image_bgr         = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        image_gray        = np.array([[2, 5], [8, 8], [0, 1]], np.uint8)
        image_3ch         = np.array([[[2,2,2], [5,5,5]], [[8,8,8],[8,8,8]], [[0,0,0], [1,1,1]]], np.uint8)
        image_rgb_jpg     = cv2.imencode('.jpg', image_rgb)[1]
        image_bgr_jpg     = cv2.imencode('.jpg', image_bgr)[1]
        image_gray_jpg    = cv2.imencode('.jpg', image_gray)[1]

        frm_raw_rgb_rw    = Frame(image_rgb, {}, 'RGB')
        frm_raw_bgr_rw    = Frame(image_bgr, {}, 'BGR')
        frm_raw_rgb_ro    = Frame(image_rgb, {}, 'RGB').ro
        frm_raw_bgr_ro    = Frame(image_bgr, {}, 'BGR').ro
        frm_raw_gray_rw   = Frame(image_gray, {}, 'RGB')
        frm_raw_gray_ro   = Frame(image_gray, {}, 'RGB').ro

        frm_jpg_rgb       = Frame.from_jpg(image_rgb_jpg, {}, 3, 2, 'RGB')
        frm_jpg_bgr       = Frame.from_jpg(image_bgr_jpg, {}, 3, 2, 'BGR')
        frm_jpg_gray      = Frame.from_jpg(image_gray_jpg, {}, 3, 2, 'GRAY')
        frm_jpg_plus_rgb  = Frame.from_jpg(image_rgb_jpg, {}, 3, 2, 'RGB')
        frm_jpg_plus_bgr  = Frame.from_jpg(image_bgr_jpg, {}, 3, 2, 'BGR')
        frm_jpg_plus_gray = Frame.from_jpg(image_gray_jpg, {}, 3, 2, 'GRAY')

        frm_jpg_plus_rgb.image  # trigger decode
        frm_jpg_plus_bgr.image
        frm_jpg_plus_gray.image

        # .rgb

        self.assertIs(frm_raw_rgb_rw.rgb, frm_raw_rgb_rw)
        self.assertIs(frm_raw_rgb_ro.rgb, frm_raw_rgb_ro)
        self.assertIs(frm_jpg_rgb.rgb, frm_jpg_rgb)
        self.assertIs(frm_jpg_rgb.rgb._Frame__image, False)
        self.assertIs(frm_jpg_plus_rgb.rgb, frm_jpg_plus_rgb)

        self.assertIs((f := frm_raw_bgr_rw.rgb).is_rw, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_rgb))

        self.assertIs((f := frm_raw_bgr_ro.rgb).is_ro, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_rgb))

        self.assertIs((f := frm_raw_gray_rw.rgb).is_rw, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertIs((f := frm_raw_gray_ro.rgb).is_ro, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertTrue(frm_jpg_rgb.rgb.is_ro)
        self.assertTrue(frm_jpg_plus_rgb.rgb.is_ro)

        # .bgr

        self.assertIs(frm_raw_bgr_rw.bgr, frm_raw_bgr_rw)
        self.assertIs(frm_raw_bgr_ro.bgr, frm_raw_bgr_ro)
        self.assertIs(frm_jpg_bgr.bgr, frm_jpg_bgr)
        self.assertIs(frm_jpg_bgr.bgr._Frame__image, False)
        self.assertIs(frm_jpg_plus_bgr.bgr, frm_jpg_plus_bgr)

        self.assertIs((f := frm_raw_rgb_rw.bgr).is_rw, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_bgr))

        self.assertIs((f := frm_raw_rgb_ro.bgr).is_ro, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_bgr))

        self.assertIs((f := frm_raw_gray_rw.bgr).is_rw, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertIs((f := frm_raw_gray_ro.bgr).is_ro, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertTrue(frm_jpg_bgr.bgr.is_ro)
        self.assertTrue(frm_jpg_plus_bgr.bgr.is_ro)

        # .gray

        self.assertIs(frm_raw_gray_rw.gray, frm_raw_gray_rw)
        self.assertIs(frm_raw_gray_ro.gray, frm_raw_gray_ro)
        self.assertIs(frm_jpg_gray.gray, frm_jpg_gray)
        self.assertIs(frm_jpg_gray.gray._Frame__image, False)
        self.assertIs(frm_jpg_plus_gray.gray, frm_jpg_plus_gray)

        self.assertIs((f := frm_raw_rgb_rw.gray).is_rw, True)
        self.assertEqual(f.format, 'GRAY')
        self.assertTrue(aeq(f.image, image_gray))

        self.assertIs((f := frm_raw_rgb_ro.gray).is_ro, True)
        self.assertEqual(f.format, 'GRAY')
        self.assertTrue(aeq(f.image, image_gray))

        self.assertIs((f := frm_raw_bgr_rw.gray).is_rw, True)
        self.assertEqual(f.format, 'GRAY')
        self.assertTrue(aeq(f.image, image_gray))

        self.assertIs((f := frm_raw_bgr_ro.gray).is_ro, True)
        self.assertEqual(f.format, 'GRAY')
        self.assertTrue(aeq(f.image, image_gray))

        self.assertTrue(frm_jpg_gray.gray.is_ro)
        self.assertTrue(frm_jpg_plus_gray.gray.is_ro)

        # .rw_rgb

        self.assertIs(frm_raw_rgb_rw.rw_rgb, frm_raw_rgb_rw)
        self.assertIsNot(frm_raw_rgb_ro.rw_rgb, frm_raw_rgb_ro)
        self.assertIsNot(frm_jpg_rgb.rw_rgb, frm_jpg_rgb)
        self.assertIsNot(frm_jpg_plus_rgb.rw_rgb, frm_jpg_plus_rgb)

        self.assertIs((f := frm_raw_bgr_rw.rw_rgb).is_rw, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_rgb))

        self.assertIs((f := frm_raw_bgr_ro.rw_rgb).is_rw, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_rgb))

        self.assertIs((f := frm_raw_gray_rw.rw_rgb).is_rw, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertIs((f := frm_raw_gray_ro.rw_rgb).is_rw, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertTrue(frm_jpg_rgb.rw_rgb.is_rw)
        self.assertTrue(frm_jpg_plus_rgb.rw_rgb.is_rw)

        frm_jpg_rgb = Frame.from_jpg(image_rgb_jpg, {}, 3, 2, 'RGB')  # because test added an .__image

        # .rw_bgr

        self.assertIs(frm_raw_bgr_rw.rw_bgr, frm_raw_bgr_rw)
        self.assertIsNot(frm_raw_bgr_ro.rw_bgr, frm_raw_bgr_ro)
        self.assertIsNot(frm_jpg_bgr.rw_bgr, frm_jpg_bgr)
        self.assertIsNot(frm_jpg_plus_bgr.rw_bgr, frm_jpg_plus_bgr)

        self.assertIs((f := frm_raw_rgb_rw.rw_bgr).is_rw, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_bgr))

        self.assertIs((f := frm_raw_rgb_ro.rw_bgr).is_rw, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_bgr))

        self.assertIs((f := frm_raw_gray_rw.rw_bgr).is_rw, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertIs((f := frm_raw_gray_ro.rw_bgr).is_rw, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertTrue(frm_jpg_bgr.rw_bgr.is_rw)
        self.assertTrue(frm_jpg_plus_bgr.rw_bgr.is_rw)

        frm_jpg_bgr = Frame.from_jpg(image_bgr_jpg, {}, 3, 2, 'BGR')  # because test added an .__image

        # .ro_rgb

        self.assertIsNot(frm_raw_rgb_rw.ro_rgb, frm_raw_rgb_rw)
        self.assertIs(frm_raw_rgb_ro.ro_rgb, frm_raw_rgb_ro)
        self.assertIs(frm_jpg_rgb.ro_rgb, frm_jpg_rgb)
        self.assertIs(frm_jpg_rgb.ro_rgb._Frame__image, False)
        self.assertIs(frm_jpg_plus_rgb.ro_rgb, frm_jpg_plus_rgb)

        self.assertIs((f := frm_raw_bgr_rw.ro_rgb).is_ro, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_rgb))

        self.assertIs((f := frm_raw_bgr_ro.ro_rgb).is_ro, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_rgb))

        self.assertIs((f := frm_raw_gray_rw.ro_rgb).is_ro, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertIs((f := frm_raw_gray_ro.ro_rgb).is_ro, True)
        self.assertEqual(f.format, 'RGB')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertTrue(frm_jpg_rgb.ro_rgb.is_ro)
        self.assertTrue(frm_jpg_plus_rgb.ro_rgb.is_ro)

        # .ro_bgr

        self.assertIsNot(frm_raw_bgr_rw.ro_bgr, frm_raw_bgr_rw)
        self.assertIs(frm_raw_bgr_ro.ro_bgr, frm_raw_bgr_ro)
        self.assertIs(frm_jpg_bgr.ro_bgr, frm_jpg_bgr)
        self.assertIs(frm_jpg_bgr.ro_bgr._Frame__image, False)
        self.assertIs(frm_jpg_plus_bgr.ro_bgr, frm_jpg_plus_bgr)

        self.assertIs((f := frm_raw_rgb_rw.ro_bgr).is_ro, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_bgr))

        self.assertIs((f := frm_raw_rgb_ro.ro_bgr).is_ro, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_bgr))

        self.assertIs((f := frm_raw_gray_rw.ro_bgr).is_ro, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertIs((f := frm_raw_gray_ro.ro_bgr).is_ro, True)
        self.assertEqual(f.format, 'BGR')
        self.assertTrue(aeq(f.image, image_3ch))

        self.assertTrue(frm_jpg_bgr.ro_bgr.is_ro)
        self.assertTrue(frm_jpg_plus_bgr.ro_bgr.is_ro)


    def test_implementation(self):
        image_rgb         = np.array([[[1,2,3], [4,5,6]], [[7,8,9],[9,8,7]], [[1,0,0], [2,0,0]]], np.uint8)
        image_bgr         = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        image_gray        = np.array([[2, 5], [8, 8], [0, 1]], np.uint8)
        image_3ch         = np.array([[[2,2,2], [5,5,5]], [[8,8,8],[8,8,8]], [[0,0,0], [1,1,1]]], np.uint8)
        image_rgb_jpg     = cv2.imencode('.jpg', image_rgb)[1]
        image_bgr_jpg     = cv2.imencode('.jpg', image_bgr)[1]
        image_gray_jpg    = cv2.imencode('.jpg', image_gray)[1]

        frm_raw_rgb_rw    = Frame(image_rgb, {}, 'RGB')
        frm_raw_bgr_rw    = Frame(image_bgr, {}, 'BGR')
        frm_raw_rgb_ro    = Frame(image_rgb, {}, 'RGB').ro
        frm_raw_bgr_ro    = Frame(image_bgr, {}, 'BGR').ro
        frm_raw_gray_rw   = Frame(image_gray, {}, 'RGB')
        frm_raw_gray_ro   = Frame(image_gray, {}, 'RGB').ro

        frm_jpg_rgb       = Frame.from_jpg(image_rgb_jpg, {}, 3, 2, 'RGB')
        frm_jpg_bgr       = Frame.from_jpg(image_bgr_jpg, {}, 3, 2, 'BGR')
        frm_jpg_gray      = Frame.from_jpg(image_gray_jpg, {}, 3, 2, 'GRAY')
        frm_jpg_plus_rgb  = Frame.from_jpg(image_rgb_jpg, {}, 3, 2, 'RGB')
        frm_jpg_plus_bgr  = Frame.from_jpg(image_bgr_jpg, {}, 3, 2, 'BGR')
        frm_jpg_plus_gray = Frame.from_jpg(image_gray_jpg, {}, 3, 2, 'GRAY')

        frm_jpg_plus_rgb.image  # trigger decode
        frm_jpg_plus_bgr.image
        frm_jpg_plus_gray.image

        # raw_rgb_rw

        n = (f := frm_raw_rgb_rw.copy()).rw

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_rw.copy()).ro

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_rw.copy()).rgb

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_rw.copy()).bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_rw.copy()).gray

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_rw.copy()).rw_rgb

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_rw.copy()).ro_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_rw.copy()).rw_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_rw.copy()).ro_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        # raw_rgb_ro

        n = (f := frm_raw_rgb_ro.copy()).rw

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_ro.copy()).ro

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_ro.copy()).rgb

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_ro.copy()).bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_bgr, n)

        n = (f := frm_raw_rgb_ro.copy()).gray

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_ro.copy()).rw_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_ro.copy()).ro_rgb

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_ro.copy()).rw_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_rgb_ro.copy()).ro_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_bgr, n)

        # jpg_rgb

        n = (f := frm_jpg_rgb.copy()).rw

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_rgb.copy()).ro

        self.assertIs(n, f)
        self.assertIs(n._Frame__image, False)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_rgb.copy()).rgb

        self.assertIs(n, f)
        self.assertIs(n._Frame__image, False)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_rgb.copy()).bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_bgr, n)

        n = (f := frm_jpg_rgb.copy()).gray

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_rgb.copy()).rw_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_rgb.copy()).ro_rgb

        self.assertIs(n, f)
        self.assertIs(n._Frame__image, False)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_rgb.copy()).rw_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_rgb.copy()).ro_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_bgr, n)

        # jpg_plus_rgb

        n = (f := frm_jpg_plus_rgb.copy()).rw

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_rgb.copy()).ro

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_plus_rgb.copy()).rgb

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_plus_rgb.copy()).bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_bgr, n)

        n = (f := frm_jpg_plus_rgb.copy()).gray

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_rgb.copy()).rw_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_rgb.copy()).ro_rgb

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_plus_rgb.copy()).rw_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_rgb.copy()).ro_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_bgr, n)

        # raw_bgr_rw

        n = (f := frm_raw_bgr_rw.copy()).rw

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_rw.copy()).ro

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_rw.copy()).bgr

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_rw.copy()).rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_rw.copy()).gray

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_rw.copy()).rw_bgr

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_rw.copy()).ro_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_rw.copy()).rw_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_rw.copy()).ro_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        # raw_bgr_ro

        n = (f := frm_raw_bgr_ro.copy()).rw

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_ro.copy()).ro

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_ro.copy()).bgr

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_ro.copy()).rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)

        n = (f := frm_raw_bgr_ro.copy()).gray

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_ro.copy()).rw_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_ro.copy()).ro_bgr

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_ro.copy()).rw_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_bgr_ro.copy()).ro_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)

        # jpg_bgr

        n = (f := frm_jpg_bgr.copy()).rw

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_bgr.copy()).ro

        self.assertIs(n, f)
        self.assertIs(n._Frame__image, False)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_bgr.copy()).bgr

        self.assertIs(n, f)
        self.assertIs(n._Frame__image, False)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_bgr.copy()).rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)

        n = (f := frm_jpg_bgr.copy()).gray

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_bgr.copy()).rw_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_bgr.copy()).ro_bgr

        self.assertIs(n, f)
        self.assertIs(n._Frame__image, False)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_bgr.copy()).rw_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_bgr.copy()).ro_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)

        # jpg_plus_bgr

        n = (f := frm_jpg_plus_bgr.copy()).rw

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_bgr.copy()).ro

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_plus_bgr.copy()).bgr

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_plus_bgr.copy()).rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)

        n = (f := frm_jpg_plus_bgr.copy()).gray

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_bgr.copy()).rw_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_bgr.copy()).ro_bgr

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_plus_bgr.copy()).rw_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_bgr.copy()).ro_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)


        # raw_gray_rw

        n = (f := frm_raw_gray_rw.copy()).rw

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_rw.copy()).ro

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_rw.copy()).bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_rw.copy()).rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_rw.copy()).gray

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_rw.copy()).rw_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_rw.copy()).ro_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_rw.copy()).rw_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_rw.copy()).ro_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        # raw_gray_ro

        n = (f := frm_raw_gray_ro.copy()).rw

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_ro.copy()).ro

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_ro.copy()).bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_bgr, n)

        n = (f := frm_raw_gray_ro.copy()).rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)

        n = (f := frm_raw_gray_ro.copy()).gray

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_ro.copy()).rw_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_ro.copy()).ro_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_bgr, n)

        n = (f := frm_raw_gray_ro.copy()).rw_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_raw_gray_ro.copy()).ro_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)

        # jpg_gray

        n = (f := frm_jpg_gray.copy()).rw

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_gray.copy()).ro

        self.assertIs(n, f)
        self.assertIs(n._Frame__image, False)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_gray.copy()).bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_bgr, n)

        n = (f := frm_jpg_gray.copy()).rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)

        n = (f := frm_jpg_gray.copy()).gray

        self.assertIs(n, f)
        self.assertIs(n._Frame__image, False)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_gray.copy()).rw_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_gray.copy()).ro_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_bgr, n)

        n = (f := frm_jpg_gray.copy()).rw_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_gray.copy()).ro_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)

        # jpg_plus_gray

        n = (f := frm_jpg_plus_gray.copy()).rw

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_gray.copy()).ro

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_plus_gray.copy()).bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_gray.copy()).rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)

        n = (f := frm_jpg_plus_gray.copy()).gray

        self.assertIs(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2), 'GRAY'))
        self.assertTrue(n._Frame__jpg)

        n = (f := frm_jpg_plus_gray.copy()).rw_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_gray.copy()).ro_bgr

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'BGR'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_gray.copy()).rw_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertTrue(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)

        n = (f := frm_jpg_plus_gray.copy()).ro_rgb

        self.assertIsNot(n, f)
        self.assertTrue(isinstance(n._Frame__image, np.ndarray))
        self.assertFalse(n._Frame__image.flags.writeable)
        self.assertEqual(n._Frame__shapef, ((3, 2, 3), 'RGB'))
        self.assertIs(n._Frame__jpg, False)
        self.assertIs(f._Frame__ro_rgb, n)


    def test_jpg(self):
        image_rgb = np.array([[[1,2,3], [4,5,6]], [[7,8,9],[9,8,7]], [[1,0,0], [2,0,0]]], np.uint8)
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        image_jpg = cv2.imencode('.jpg', image_bgr)[1]

        self.assertRaises(AssertionError, lambda: Frame.from_jpg(image_jpg, None, 1, 1).image)

        self.assertEqual(Frame.from_jpg(image_jpg).shape, (3, 2, 3))
        self.assertEqual(Frame.from_jpg(image_jpg, format='GRAY').shape, (3, 2))
        self.assertEqual(Frame.from_jpg(image_jpg, format='GRAY').format, 'GRAY')
        self.assertEqual(Frame.from_jpg(image_jpg, format='RGB').format, 'RGB')
        self.assertEqual(Frame.from_jpg(image_jpg, format='BGR').format, 'BGR')


    def test_eq(self):
        image_rgb        = np.array([[[1,2,3], [4,5,6]], [[7,8,9],[9,8,7]], [[1,0,0], [2,0,0]]], np.uint8)
        image_bgr        = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        image_jpg        = cv2.imencode('.jpg', image_bgr)[1]
        frm_raw_rgb_rw   = Frame(image_rgb, {}, 'RGB')
        frm_raw_bgr_rw   = Frame(image_bgr, {}, 'BGR')
        frm_raw_rgb_ro   = Frame(image_rgb, {}, 'RGB').ro
        frm_raw_bgr_ro   = Frame(image_bgr, {}, 'BGR').ro
        frm_jpg_rgb      = Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB')
        frm_jpg_bgr      = Frame.from_jpg(image_jpg, {}, 3, 2, 'BGR')
        frm_plus_jpg_rgb = Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB').ro
        frm_plus_jpg_bgr = Frame.from_jpg(image_jpg, {}, 3, 2, 'BGR').ro

        frm_plus_jpg_rgb.image  # trigger decode
        frm_plus_jpg_bgr.image

        self.assertEqual(frm_raw_rgb_rw, frm_raw_rgb_rw)
        self.assertEqual(frm_raw_bgr_rw, frm_raw_bgr_rw)
        self.assertEqual(frm_raw_rgb_ro, frm_raw_rgb_ro)
        self.assertEqual(frm_raw_bgr_ro, frm_raw_bgr_ro)
        self.assertEqual(frm_jpg_rgb, frm_jpg_rgb)
        self.assertEqual(frm_jpg_bgr, frm_jpg_bgr)
        self.assertEqual(frm_plus_jpg_rgb, frm_plus_jpg_rgb)
        self.assertEqual(frm_plus_jpg_bgr, frm_plus_jpg_bgr)

        self.assertEqual(frm_raw_rgb_rw, frm_raw_rgb_ro)
        self.assertEqual(frm_raw_bgr_rw, frm_raw_bgr_ro)
        self.assertEqual(frm_jpg_rgb, frm_plus_jpg_rgb)
        self.assertEqual(frm_jpg_bgr, frm_plus_jpg_bgr)

        self.assertNotEqual(frm_raw_rgb_rw, frm_raw_bgr_rw)
        self.assertNotEqual(frm_raw_rgb_ro, frm_raw_bgr_ro)

        self.assertNotEqual(frm_raw_rgb_rw, None)
        self.assertNotEqual(frm_raw_bgr_rw, None)
        self.assertNotEqual(frm_raw_rgb_ro, None)
        self.assertNotEqual(frm_raw_bgr_ro, None)
        self.assertNotEqual(frm_jpg_rgb, None)
        self.assertNotEqual(frm_jpg_bgr, None)
        self.assertNotEqual(frm_plus_jpg_rgb, None)
        self.assertNotEqual(frm_plus_jpg_bgr, None)
        self.assertNotEqual(frm_raw_rgb_rw, None)
        self.assertNotEqual(frm_raw_bgr_rw, None)
        self.assertNotEqual(frm_jpg_rgb, None)
        self.assertNotEqual(frm_jpg_bgr, None)


    def test_serialize(self):
        sig = lambda f: (f._Frame__data, f._Frame__jpg, f._Frame__shapef,
            (i.flags.writeable, bytes(i)) if isinstance(i := f._Frame__image, np.ndarray) else None)

        image_rgb        = np.array([[[1,2,3], [4,5,6]], [[7,8,9],[9,8,7]], [[1,0,0], [2,0,0]]], np.uint8)
        image_bgr        = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        image_jpg        = cv2.imencode('.jpg', image_bgr)[1]
        frm_raw_rgb_rw   = Frame(image_rgb, {}, 'RGB')
        frm_raw_bgr_rw   = Frame(image_bgr, {}, 'BGR')
        frm_raw_rgb_ro   = Frame(image_rgb, {}, 'RGB').ro
        frm_raw_bgr_ro   = Frame(image_bgr, {}, 'BGR').ro
        frm_jpg_rgb      = Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB')
        frm_jpg_bgr      = Frame.from_jpg(image_jpg, {}, 3, 2, 'BGR')
        frm_plus_jpg_rgb = Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB').ro
        frm_plus_jpg_bgr = Frame.from_jpg(image_jpg, {}, 3, 2, 'BGR').ro

        frm_plus_jpg_rgb.image  # trigger decode
        frm_plus_jpg_bgr.image

        self.assertEqual(sig(frm_raw_rgb_rw), sig(pickle.loads(pickle.dumps(frm_raw_rgb_rw))))
        self.assertEqual(sig(frm_raw_bgr_rw), sig(pickle.loads(pickle.dumps(frm_raw_bgr_rw))))
        self.assertEqual(sig(frm_raw_rgb_ro), sig(pickle.loads(pickle.dumps(frm_raw_rgb_ro))))
        self.assertEqual(sig(frm_raw_bgr_ro), sig(pickle.loads(pickle.dumps(frm_raw_bgr_ro))))
        self.assertEqual(sig(frm_jpg_rgb), sig(pickle.loads(pickle.dumps(frm_jpg_rgb))))
        self.assertEqual(sig(frm_jpg_bgr), sig(pickle.loads(pickle.dumps(frm_jpg_bgr))))
        self.assertEqual(sig(frm_plus_jpg_rgb), sig(pickle.loads(pickle.dumps(frm_plus_jpg_rgb))))
        self.assertEqual(sig(frm_plus_jpg_bgr), sig(pickle.loads(pickle.dumps(frm_plus_jpg_bgr))))


    def test_init(self):
        image_rgb        = np.array([[[1,2,3], [4,5,6]], [[7,8,9],[9,8,7]], [[1,0,0], [2,0,0]]], np.uint8)
        image_bgr        = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        image_jpg        = cv2.imencode('.jpg', image_bgr)[1]
        frm_raw_rgb_rw   = Frame(image_rgb, {}, 'RGB')
        frm_raw_bgr_rw   = Frame(image_bgr, {'other': True}, 'BGR')
        frm_raw_rgb_ro   = Frame(image_rgb, {}, 'RGB').ro
        frm_raw_bgr_ro   = Frame(image_bgr, {}, 'BGR').ro
        frm_jpg_rgb      = Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB')
        frm_jpg_bgr      = Frame.from_jpg(image_jpg, {}, 3, 2, 'BGR')
        frm_plus_jpg_rgb = Frame.from_jpg(image_jpg, {}, 3, 2, 'RGB')
        frm_plus_jpg_bgr = Frame.from_jpg(image_jpg, {}, 3, 2, 'BGR')

        frm_plus_jpg_rgb.image  # trigger decode
        frm_plus_jpg_bgr.image

        f = Frame(frm_raw_rgb_rw)

        self.assertIs(f._Frame__image, frm_raw_rgb_rw._Frame__image)
        self.assertIs(f._Frame__data, frm_raw_rgb_rw._Frame__data)
        self.assertIs(f._Frame__shapef, frm_raw_rgb_rw._Frame__shapef)
        self.assertEqual(f._Frame__jpg, frm_raw_rgb_rw._Frame__jpg)

        f = Frame(frm_jpg_rgb)

        self.assertIs(f._Frame__image, frm_jpg_rgb._Frame__image)
        self.assertIs(f._Frame__data, frm_jpg_rgb._Frame__data)
        self.assertIs(f._Frame__shapef, frm_jpg_rgb._Frame__shapef)
        self.assertEqual(f._Frame__jpg, frm_jpg_rgb._Frame__jpg)

        f = Frame(frm_plus_jpg_bgr)

        self.assertIs(f._Frame__image, frm_plus_jpg_bgr._Frame__image)
        self.assertIs(f._Frame__data, frm_plus_jpg_bgr._Frame__data)
        self.assertIs(f._Frame__shapef, frm_plus_jpg_bgr._Frame__shapef)
        self.assertEqual(f._Frame__jpg, frm_plus_jpg_bgr._Frame__jpg)

        f = Frame(frm_raw_rgb_rw, {'other': True})

        self.assertIs(f._Frame__image, frm_raw_rgb_rw._Frame__image)
        self.assertEqual(f._Frame__data, {'other': True})
        self.assertIs(f._Frame__shapef, frm_raw_rgb_rw._Frame__shapef)
        self.assertEqual(f._Frame__jpg, frm_raw_rgb_rw._Frame__jpg)

        f = Frame(frm_raw_rgb_rw, frm_raw_bgr_rw)

        self.assertIs(f._Frame__image, frm_raw_rgb_rw._Frame__image)
        self.assertIs(f._Frame__data, frm_raw_bgr_rw._Frame__data)
        self.assertIs(f._Frame__shapef, frm_raw_rgb_rw._Frame__shapef)
        self.assertEqual(f._Frame__jpg, frm_raw_rgb_rw._Frame__jpg)

        f = Frame(frm_raw_rgb_rw, format='BGR')

        self.assertIs(f._Frame__image, frm_raw_rgb_rw._Frame__image)
        self.assertIs(f._Frame__data, frm_raw_rgb_rw._Frame__data)
        self.assertEqual(f.shape, frm_raw_rgb_rw.shape)
        self.assertEqual(f.format, 'BGR')

        f = Frame(frm_jpg_bgr, frm_raw_bgr_rw, frm_raw_rgb_rw)

        self.assertIs(f._Frame__image, frm_jpg_bgr._Frame__image)
        self.assertIs(f._Frame__data, frm_raw_bgr_rw._Frame__data)
        self.assertIs(f._Frame__jpg, frm_jpg_bgr._Frame__jpg)
        self.assertEqual(f.shape, frm_jpg_bgr.shape)
        self.assertEqual(f.format, frm_raw_rgb_rw.format)

        f = Frame(frm_raw_rgb_rw)

        self.assertIs(f._Frame__image, frm_raw_rgb_rw._Frame__image)
        self.assertIs(f._Frame__data, frm_raw_rgb_rw._Frame__data)
        self.assertIs(f._Frame__shapef, frm_raw_rgb_rw._Frame__shapef)
        self.assertEqual(f._Frame__jpg, frm_raw_rgb_rw._Frame__jpg)

        f = Frame(image_rgb, {'other': True}, 'BGR')

        self.assertIs(f._Frame__image, frm_raw_rgb_rw._Frame__image)
        self.assertEqual(f._Frame__data, {'other': True})
        self.assertEqual(f.shape, image_rgb.shape)
        self.assertEqual(f.format, 'BGR')
        self.assertEqual(f._Frame__jpg, False)

        f = Frame(image_rgb, {'other': True}, frm_raw_rgb_rw)

        self.assertIs(f._Frame__image, frm_raw_rgb_rw._Frame__image)
        self.assertEqual(f._Frame__data, {'other': True})
        self.assertEqual(f.shape, image_rgb.shape)
        self.assertEqual(f.format, frm_raw_rgb_rw.format)
        self.assertEqual(f._Frame__jpg, False)

        f = Frame(image_rgb, frm_raw_bgr_rw)

        self.assertIs(f._Frame__image, frm_raw_rgb_rw._Frame__image)
        self.assertIs(f._Frame__data, frm_raw_bgr_rw._Frame__data)
        self.assertEqual(f.shape, image_rgb.shape)
        self.assertEqual(f.format, frm_raw_bgr_rw.format)
        self.assertEqual(f._Frame__jpg, False)


if __name__ == '__main__':
    unittest.main()
