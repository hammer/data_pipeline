
import unittest

import mrtarget.common as common
from toolz import curry, take
from tempfile import NamedTemporaryFile
import os
from mrtarget.common import URLZSource, LogAccum
from toolz.functoolz import compose
from string import rstrip


class DataStructureTests(unittest.TestCase):
    def test_url_to_stream(self):

        lines4 = \
            list(take(4, common.url_to_stream("http://www.google.com/robots.txt")))

        self.assertGreaterEqual(len(lines4), 1, "Failed to get more than 0 lines")

    def test_urlzsource(self):
        lines4 = []
        with URLZSource('http://www.google.com/robots.txt').open() as f:
            take_and_rstrip = compose(curry(map,
                                            lambda l: rstrip(l, '\n')),
                                      curry(take, 4))
            lines4 = list(take_and_rstrip(f))

        print(str(lines4))
        self.assertGreaterEqual(len(lines4), 1,
                              "Failed to get more than 0 lines")

    def test_log_accum(self):
        def partial_class(cls, *args, **kwds):
            '''the way to generate partial from a constructor'''
            class NewCls(cls):
                __init__ = curry(cls.__init__, *args, **kwds)

            return NewCls


        log_accum_none = partial_class(LogAccum, logger_o=None)
        self.assertRaises(TypeError, log_accum_none)

        import logging as _l
        logger = _l.getLogger(__name__)

        la = LogAccum(logger)

        la.log(_l.ERROR, 'log message 1')
        la.log(_l.ERROR, 'log message 2')

        self.assertGreater(la._accum['counter'], 0, 'it should be 2 messages so > 0')

        la.flush()
        self.assertEqual(la._accum['counter'], 0, 'it cannot contain messages')
