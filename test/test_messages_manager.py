#!/usr/bin/env python
# coding: utf-8
import unittest
from tempfile import mkstemp

from messages_manager import Aggregate, AggregatesParser, MessagesManager


class test_aggregation(unittest.TestCase):

    def test_no_aggregate(self):
        output = mkstemp()[1]
        agg = Aggregate(output, ['test/data/messages_en_US.properties', 'test/data/messages_en_US_from_addon.properties'])
        MessagesManager([agg]).aggregate(None)
        self.assertEqual("""## DO NOT EDIT FOLLOWING LINE
# Translations from test/data/messages_en_US.properties
label.foo=Bar
label.truc=Chouette

label.bidule=yo

## DO NOT EDIT FOLLOWING LINE
# Translations from test/data/messages_en_US_from_addon.properties
label.fii=bur""", self.getResult(output));

    def test_aggregate(self):
        output = mkstemp()[1]
        agg = Aggregate(output, ['test/data/messages_en_US.properties'])
        MessagesManager([agg]).aggregate(None)
        self.assertEqual("""## DO NOT EDIT FOLLOWING LINE
# Translations from test/data/messages_en_US.properties
label.foo=Bar
label.truc=Chouette

label.bidule=yo""", self.getResult(output));

    def test_no_split(self):
        output = mkstemp()[1]
        agg = Aggregate('test/data/aggs/messages_en_US_not_aggregated.properties', [output])
        MessagesManager([agg]).split(None)
        # first filepath is kept because it uses another path than temp test file
        self.assertEqual("""# test/data/messages_en_US.properties
label.foo=Bar
label.truc=Chouette

label.bidule=yo""", self.getResult(output));

    def test_split(self):
        output1 = mkstemp()[1]
        output2 = mkstemp()[1]
        agg = Aggregate('test/data/aggs/messages_en_US_aggregated.properties', [output1, output2])
        MessagesManager([agg]).split(None)

        # first filepath is kept because it uses another path than temp test file

        self.assertEqual("""# test/data/messages_en_US.properties
label.foo=Bar
label.truc=Chouette

label.bidule=yo

""", self.getResult(output1));

        self.assertEqual("""# test/data/messages_en_US_from_addon.properties
label.fii=bur""", self.getResult(output2));

    def getResult(self, output):
        try:
            f = open(output, 'r')
            return f.read()
        finally:
            f.close()


class test_parser(unittest.TestCase):

    def test_parser_unknown_project(self):
        ap = AggregatesParser()
        #res = ap.load('test/data', 'foo')
        #self.assertEqual(0, len(res))

    def test_parser_none_project(self):
        ap = AggregatesParser()
        res = ap.load('test/data', None)
        self.assertEqual(0, len(res))

    def test_parser_nuxeo_project(self):
        ap = AggregatesParser()
        res = ap.load('test/data', 'nuxeo')
        self.assertEqual(3, len(res))
        self.assertTrue('en_US' in res)
        self.assertEqual(3, len(res['en_US']))
        self.assertEqual('test/data/addon/messages_en_US.properties', res['en_US'][0])
        self.assertEqual('test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_en_US.properties', res['en_US'][1])
        self.assertEqual('test/data/nuxeo/nuxeo-other/messages_en_US.properties', res['en_US'][2])
        self.assertTrue('fr_FR' in res)
        self.assertEqual(1, len(res['fr_FR']))
        self.assertEqual('test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_fr_FR.properties', res['fr_FR'][0])
        self.assertTrue('pt_BR' in res)
        self.assertEqual(1, len(res['pt_BR']))
        self.assertEqual('test/data/nuxeo/addons/nuxeo-platform-lang-ext/messages_pt_BR.properties', res['pt_BR'][0])

    def test_parser_nuxeo_project_no_addon(self):
        ap = AggregatesParser()
        res = ap.load('test/data/nuxeo', 'nuxeo')
        self.assertEqual(3, len(res))
        self.assertTrue('en_US' in res)
        self.assertEqual(2, len(res['en_US']))
        self.assertEqual('test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_en_US.properties', res['en_US'][0])
        self.assertEqual('test/data/nuxeo/nuxeo-other/messages_en_US.properties', res['en_US'][1])

    def test_parser_multiple(self):
        ap = AggregatesParser(crowdin='crowdin_multiple.ini')
        res = ap.load('test/data', 'nuxeo')
        self.assertEqual(1, len(res))
        self.assertTrue('en_US' in res)
        self.assertEqual(2, len(res['en_US']))
        self.assertEqual('test/data/addon/messages_en_US.properties', res['en_US'][0])
        self.assertEqual('test/data/addon/messages_en_US_from_addon.properties', res['en_US'][1])
