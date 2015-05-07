#!/usr/bin/env python

import unittest
from nose.tools import assert_equal, assert_true
from crowdin_updater import CrowdinUpdater
from tempfile import mkstemp

class test_crowding_updater(unittest.TestCase):

    def test_build_invalid(self):
        cu = CrowdinUpdater('nuxeo', 'foo')
        self.assertRaises(ValueError, cu.build)

    def test_download_invalid(self):
        cu = CrowdinUpdater('nuxeo', 'foo')
        self.assertRaises(ValueError, cu.download, 'target')
