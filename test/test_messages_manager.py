#!/usr/bin/env python

import unittest
from nose.tools import assert_equal, assert_true
from messages_manager import Aggregate, MessagesManager
from tempfile import mkstemp

class test_messages_aggregator(unittest.TestCase):

    def test_no_aggregate(self):
        output = mkstemp()[1]
        agg = Aggregate(output, ["test/data/messages_en_US.properties", "test/data/messages_en_US_from_addon.properties"])
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
        agg = Aggregate(output, ["test/data/messages_en_US.properties"])
        MessagesManager([agg]).aggregate(None)
        assert_equal("""## DO NOT EDIT FOLLOWING LINE
# test/data/messages_en_US.properties
label.foo=Bar
label.truc=Chouette

label.bidule=yo""", self.getResult(output));

    def test_no_split(self):
        output = mkstemp()[1]
        agg = Aggregate("test/data/messages_en_US_not_aggregated.properties", [output])
        MessagesManager([agg]).split(None)
        # first filepath is kept because it uses another path than temp test file
        assert_equal("""# test/data/messages_en_US.properties
label.foo=Bar
label.truc=Chouette

label.bidule=yo""", self.getResult(output));

    def test_split(self):
        output1 = mkstemp()[1]
        output2 = mkstemp()[1]
        agg = Aggregate("test/data/messages_en_US_aggregated.properties", [output1, output2])
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
