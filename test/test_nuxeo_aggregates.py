#!/usr/bin/env python

import unittest
from nose.tools import assert_equal, assert_true
from nuxeo_aggregates import NXAGGS, NXAGGS_EXT, NXAGGS_ALL

class test_messages_aggregator(unittest.TestCase):

    def test_nux_aggregates(self):
        assert_equal(2, len(NXAGGS))
        assert_equal(21, len(NXAGGS_EXT))
        assert_equal(23, len(NXAGGS_ALL))
