#!/usr/bin/env python

import unittest
from nose.tools import assert_equal, assert_true
from messages_manager import Aggregate, AggregatesParser, MessagesManager
from tempfile import mkstemp

class test_aggregation(unittest.TestCase):

    def test_no_aggregate(self):
        output = mkstemp()[1]
        agg = Aggregate(output, ['test/data/messages_en_US.properties', 'test/data/messages_en_US_from_addon.properties'])
        MessagesManager([agg]).aggregate(None)
        assert_equal("""## DO NOT EDIT FOLLOWING LINE
# test/data/messages_en_US.properties
label.foo=Bar
label.truc=Chouette

label.bidule=yo

## DO NOT EDIT FOLLOWING LINE
# test/data/messages_en_US_from_addon.properties
label.fii=bur""", self.getResult(output));

    def test_aggregate(self):
        output = mkstemp()[1]
        agg = Aggregate(output, ['test/data/messages_en_US.properties'])
        MessagesManager([agg]).aggregate(None)
        assert_equal("""## DO NOT EDIT FOLLOWING LINE
# test/data/messages_en_US.properties
label.foo=Bar
label.truc=Chouette

label.bidule=yo""", self.getResult(output));

    def test_no_split(self):
        output = mkstemp()[1]
        agg = Aggregate('test/data/aggs/messages_en_US_not_aggregated.properties', [output])
        MessagesManager([agg]).split(None)
        # first filepath is kept because it uses another path than temp test file
        assert_equal("""# test/data/messages_en_US.properties
label.foo=Bar
label.truc=Chouette

label.bidule=yo""", self.getResult(output));

    def test_split(self):
        output1 = mkstemp()[1]
        output2 = mkstemp()[1]
        agg = Aggregate('test/data/aggs/messages_en_US_aggregated.properties', [output1, output2])
        MessagesManager([agg]).split(None)

        # first filepath is kept because it uses another path than temp test file

        assert_equal("""# test/data/messages_en_US.properties
label.foo=Bar
label.truc=Chouette

label.bidule=yo

""", self.getResult(output1));

        assert_equal("""# test/data/messages_en_US_from_addon.properties
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
        #assert_equal(0, len(res))

    def test_parser_none_project(self):
        ap = AggregatesParser()
        res = ap.load('test/data', None)
        assert_equal(0, len(res))

    def test_parser_nuxeo_project(self):
        ap = AggregatesParser()
        res = ap.load('test/data', 'nuxeo')
        assert_equal(3, len(res))
        assert_true('en_US' in res)
        assert_equal(3, len(res['en_US']))
        assert_equal('test/data/addon/messages_en_US.properties', res['en_US'][0])
        assert_equal('test/data/nuxeo/nuxeo-other/messages_en_US.properties', res['en_US'][1])
        assert_equal('test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_en_US.properties', res['en_US'][2])
        assert_true('fr_FR' in res)
        assert_equal(1, len(res['fr_FR']))
        assert_equal('test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_fr_FR.properties', res['fr_FR'][0])
        assert_true('pt_BR' in res)
        assert_equal(1, len(res['pt_BR']))
        assert_equal('test/data/nuxeo/addons/nuxeo-platform-lang-ext/messages_pt_BR.properties', res['pt_BR'][0])

    def test_parser_nuxeo_project_no_addon(self):
        ap = AggregatesParser()
        res = ap.load('test/data/nuxeo', 'nuxeo')
        assert_equal(3, len(res))
        assert_true('en_US' in res)
        assert_equal(2, len(res['en_US']))
        assert_equal('test/data/nuxeo/nuxeo-other/messages_en_US.properties', res['en_US'][0])
        assert_equal('test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_en_US.properties', res['en_US'][1])

    def test_parser_multiple(self):
        ap = AggregatesParser(crowdin='crowdin_multiple.ini')
        res = ap.load('test/data', 'nuxeo')
        assert_equal(1, len(res))
        assert_true('en_US' in res)
        assert_equal(2, len(res['en_US']))
        assert_equal('test/data/addon/messages_en_US.properties', res['en_US'][0])
        assert_equal('test/data/addon/messages_en_US_from_addon.properties', res['en_US'][1])
