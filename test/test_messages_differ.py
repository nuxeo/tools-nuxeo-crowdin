#!/usr/bin/env python

import unittest, os
from nose.tools import assert_equal
from messages_differ import Differ

class test_messages_differ(unittest.TestCase):

    def test_diff(self):
        diff = Differ('test/data/messages_en_US.properties', 'test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_en_US.properties').diff()
        assert_equal(4, len(diff))
        assert_equal('label.foo', diff[0].name)
        assert_equal('Bar', diff[0].one)
        assert_equal(None, diff[0].other)
        assert_equal('label.truc', diff[1].name)
        assert_equal('Chouette', diff[1].one)
        assert_equal('Chouette2', diff[1].other)
        assert_equal('label.bidule', diff[2].name)
        assert_equal('yo', diff[2].one)
        assert_equal(None, diff[2].other)
        assert_equal('label.lang', diff[3].name)
        assert_equal(None, diff[3].one)
        assert_equal('Foo engl', diff[3].other)

