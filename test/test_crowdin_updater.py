#!/usr/bin/env python

import os
import unittest
from nose.tools import assert_equal, assert_true
from crowdin_updater import CrowdinUpdater
from tempfile import mkstemp

class test_crowding_updater(unittest.TestCase):

    def test_missing_key(self):
        del os.environ['CROWDIN_API_KEY']
        self.assertRaises(ValueError, CrowdinUpdater, 'nuxeo')

    def test_build_invalid(self):
        os.environ['CROWDIN_API_KEY'] = 'foo'
        cu = CrowdinUpdater('nuxeo')
        self.assertRaises(ValueError, cu.build)

    def test_download_invalid(self):
        os.environ['CROWDIN_API_KEY'] = 'foo'
        cu = CrowdinUpdater('nuxeo')
        self.assertRaises(ValueError, cu.download, 'target')
