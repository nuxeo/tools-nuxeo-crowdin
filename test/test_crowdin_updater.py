#!/usr/bin/env python
# coding: utf-8
import os
import unittest

from crowdin_updater import CrowdinUpdater


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
