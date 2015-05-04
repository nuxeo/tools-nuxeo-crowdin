#!/usr/bin/env python

import unittest, os
from nose.tools import assert_equal, assert_true
from nuxeo_aggregates import aggregate
from tempfile import mkdtemp

class test_nuxeo_aggregates(unittest.TestCase):

    def test_nux_aggregates(self):
        outputdir = mkdtemp()
        aggregate('test/data/nuxeo', outputdir)
        res = self.getResult(outputdir)
        assert_equal(2, len(res))
        assert_equal('./messages.properties', res[0][0])
        assert_equal("""## DO NOT EDIT FOLLOWING LINE
# test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_en_US.properties
label.lang=Foo engl
label.truc=Chouette2""", res[0][1])
        assert_equal('fr/messages_fr_FR.properties', res[1][0])
        assert_equal("""## DO NOT EDIT FOLLOWING LINE
# test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_fr_FR.properties
label.lang=Foo french""", res[1][1])

    def test_nux_aggregates_ext(self):
        outputdir = mkdtemp()
        aggregate('test/data/nuxeo', outputdir, ext=True)
        res = self.getResult(outputdir)
        assert_equal(1, len(res))
        assert_equal('pt_BR/messages_pt_BR.properties', res[0][0])
        assert_equal("""## DO NOT EDIT FOLLOWING LINE
# test/data/nuxeo/addons/nuxeo-platform-lang-ext/messages_pt_BR.properties
label.lang=Foo Br""", res[0][1])

    def test_nux_aggregates_all(self):
        outputdir = mkdtemp()
        aggregate('test/data/nuxeo', outputdir, all=True)
        res = self.getResult(outputdir)
        assert_equal(3, len(res))
        assert_equal('./messages.properties', res[0][0])
        assert_equal("""## DO NOT EDIT FOLLOWING LINE
# test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_en_US.properties
label.lang=Foo engl
label.truc=Chouette2

## DO NOT EDIT FOLLOWING LINE
# test/data/nuxeo/nuxeo-other/messages_en_US.properties
label.foo=Bar
label.truc=Chouette

label.bidule=yo""", res[0][1])
        assert_equal('fr/messages_fr_FR.properties', res[1][0])
        assert_equal("""## DO NOT EDIT FOLLOWING LINE
# test/data/nuxeo/nuxeo-features/nuxeo-platform-lang/messages_fr_FR.properties
label.lang=Foo french""", res[1][1])
        assert_equal('pt_BR/messages_pt_BR.properties', res[2][0])
        assert_equal("""## DO NOT EDIT FOLLOWING LINE
# test/data/nuxeo/addons/nuxeo-platform-lang-ext/messages_pt_BR.properties
label.lang=Foo Br""", res[2][1])

    def getResult(self, output):
        res = []
        for path, subdirs, files in os.walk(output):
            for filename in files:
                fpath = os.path.join(path, filename)
                f = None
                try:
                    f = open(fpath, 'r')
                    res.append((os.path.join(os.path.relpath(path, output), filename), f.read()))
                finally:
                    if f is not None:
                        f.close()
        return res
