#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Handles diff of a tree of messages files
"""

import os, StringIO, ConfigParser

class Differ:
    """
    Helper class with diff methods to compare messages files
    """
    def __init__(self, src, dst):
        self.src = self.getConfig(src)
        self.dst = self.getConfig(dst)

    def getConfig(self, filepath):
        conf = StringIO.StringIO()
        conf.write('[foo]\n')
        conf.write(open(filepath).read())
        conf.seek(0, os.SEEK_SET)
        c = ConfigParser.ConfigParser()
        c.readfp(conf)
        return c

    def getMissingDestKeys(self):
        return self.getMissingKeys(self.src, self.dst)

    def getAdditionalDestKeys(self):
        return self.getMissingKeys(self.dst, self.src)

    def getMissingKeys(self, src, dst):
        missing = []
        for option in src.options("foo"):
            if not dst.has_option("foo", option):
                missing.append(option)
        missing.sort()
        return missing

    def diff(self):
        diffs = []
        for option in self.src.options("foo"):
            sval = self.src.get("foo", option)
            if not self.dst.has_option("foo", option):
                diffs.append(Diff(option, sval, None))
                continue
            dval = self.dst.get("foo", option)
            if sval != dval:
                diffs.append(Diff(option, sval, dval))

        # handle potential additional keys
        added = self.getAdditionalDestKeys()
        for a in added:
            diffs.append(Diff(a, None, self.dst.get("foo", a)))

        return diffs

class Diff:
    """
    Represents a diff
    """
    def __init__(self, name, one, other):
        self.name = name
        self.one = one
        self.other = other

    def __str__(self):
        return "{%s: '%s'!='%s'}" %(self.name, self.one, self.other,)

    def __repr__(self):
        return self.__str__()

