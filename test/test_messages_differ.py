#!/usr/bin/env python
# coding: utf-8
import unittest

from messages_differ import Differ


class test_messages_differ(unittest.TestCase):

    def test_diff(self):
        diff = Differ('test/data/messages_en_US.properties', 'test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_en_US.properties').diff()
        self.assertEqual(4, len(diff))
        self.assertEqual('label.foo', diff[0].name)
        self.assertEqual('Bar', diff[0].one)
        self.assertEqual(None, diff[0].other)
        self.assertEqual('label.truc', diff[1].name)
        self.assertEqual('Chouette', diff[1].one)
        self.assertEqual('Chouette2', diff[1].other)
        self.assertEqual('label.bidule', diff[2].name)
        self.assertEqual('yo', diff[2].one)
        self.assertEqual(None, diff[2].other)
        self.assertEqual('label.lang', diff[3].name)
        self.assertEqual(None, diff[3].one)
        self.assertEqual('Foo engl', diff[3].other)

