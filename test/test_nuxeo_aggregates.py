#!/usr/bin/env python

import unittest
from nose.tools import assert_equal, assert_true
from nuxeo_aggregates import NXAGGS

class test_messages_aggregator(unittest.TestCase):

    def test_nux_aggregates(self):
        assert_equal(23, len(NXAGGS))
