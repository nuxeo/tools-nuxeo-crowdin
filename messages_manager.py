#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Handles aggregation of messages* files from a given list of repositories
"""

import string, sys, os
import ConfigParser

class Aggregate:
    """
    Represents an aggregated version of messages.
    """
    def __init__(self, targetpath, origpaths):
        self.targetpath = targetpath
        self.origpaths = origpaths

    def __str__(self):
        return "Aggregate target='%s', paths='%s'" %(self.targetpath, self.origpaths,)

    def __repr__(self):
        return self.__str__()

class AggregatesParser:
    """
    Detects aggregates to takes into account given a base directory,
    looking fro crowding.ini files in the tree.

    The additional project argument can be used to filter confiuration
    from crowdin.ini files and gather files for different use cases.
    """
    def __init__(self, crowdin="crowdin.ini"):
        self.crowdin = crowdin

    """
    Returns a map with language as key, and lists of paths to messages as value.
    """
    def load(self, dir, project, excluded_dirs=[]):
        res = {}
        # TODO: optimize lookup of files (use glob?)
        for path, subdirs, files in os.walk(dir):
            if os.path.relpath(path, dir) in excluded_dirs:
                continue
            for filename in files:
                if filename != self.crowdin:
                    continue
                f = os.path.join(path, filename)
                if f in excluded_dirs:
                    continue
                c = ConfigParser.ConfigParser()
                c.optionxform = str
                c.read(f)
                if not c.has_section(project):
                    continue
                for lang in c.options(project):
                    val = c.get(project, lang)
                    mpaths = []
                    if "," in val:
                        # handle multiple use case
                        for p in val.split(','):
                            mpaths.append(os.path.join(path, p.strip()))
                    else:
                        mpaths.append(os.path.join(path, val.strip()))
                    if lang in res:
                        res[lang].extend(mpaths)
                    else:
                        res[lang] = mpaths
                    # sort for deterministic behaviour
                    res[lang].sort()
        return res

class MessagesManager:
    """
    Aggregates and splits message files according to given list of Aggregate objects.
    """
    def __init__(self, aggregates):
        self.aggregates = aggregates

    def aggregate(self, outputdir):
        for aggregate in self.aggregates:
            if len(aggregate.origpaths) > 1:
                # aggregate content and copy to target file
                i = 0
                for origpath in aggregate.origpaths:
                    outpath = os.path.join(outputdir, aggregate.targetpath)
                    if i == 0:
                        self.writeAggregated(origpath, outpath, 'w')
                    else:
                        self.writeAggregated(origpath, outpath, 'a', start=False)
                    i += 1
            else:
                # just copy the content to target file
                outpath = os.path.join(outputdir, aggregate.targetpath)
                self.writeAggregated(aggregate.origpaths[0], outpath, 'w')

    def writeAggregated(self, filepath, targetpath, mode, start=True):
        fi = self.open(filepath, 'r')
        fo = self.open(targetpath, mode, mkdir=True)
        if not start:
            fo.write("\n\n")
        fo.write("## DO NOT EDIT FOLLOWING LINE\n")
        fo.write("# Translations from " + filepath + "\n")
        try:
            nbEmpty = 0
            for line in fi:

                (stillEmpty, nbEmpty) = self.handle_empty(line, nbEmpty, fo)
                if stillEmpty is True:
                    continue

                fo.write(line)

        finally:
            fi.close()
            fo.close()

    def split(self, outputdir):
        for aggregate in self.aggregates:
            self.writeSplit(aggregate.targetpath, outputdir, aggregate.origpaths)

    def writeSplit(self, filepath, outputdir, targetpaths):
        if len(targetpaths) > 1:
            # just copy back content to target file, removing header
            fi = self.open(filepath, 'r')
            fo = None
            i = 0
            current = os.path.join(outputdir, targetpaths[i])
            try:
                j = 0
                nbEmpty = 0
                for line in fi:

                    (stillEmpty, nbEmpty) = self.handle_empty(line, nbEmpty, fo)
                    if stillEmpty is True:
                        continue

                    if "## DO NOT EDIT FOLLOWING LINE\n" == line:
                        # open next targetpath
                        if fo is not None:
                            fo.close()
                        current = os.path.join(outputdir, targetpaths[i])
                        i += 1
                        fo = self.open(current, 'w', mkdir=True)
                        j = 0
                        continue
                    elif (j == 0 or j == 1) and (line.startswith("# Translations from " + current)):
                        continue
                    elif nbEmpty < 1:
                        fo.write(line)
                    j += 1
            finally:
                fi.close()
                if fo is not None:
                    fo.close()
        else:
            # just copy back content to target file, removing header
            fi = self.open(filepath, 'r')
            fo = self.open(targetpaths[0], 'w', mkdir=True)
            try:
                i = 0
                nbEmpty = 0
                for line in fi:
                    (stillEmpty, nbEmpty) = self.handle_empty(line, nbEmpty, fo)

                    if i == 0 and "## DO NOT EDIT FOLLOWING LINE\n" == line:
                        continue
                    elif (i == 0 or i == 1) and (line.startswith("# " + filepath)):
                        continue
                    elif nbEmpty < 1:
                        fo.write(line)
                    i += 1
            finally:
                fi.close()
                fo.close()

    def handle_empty(self, line, nbEmpty, out):
        if not line.rstrip():
            return (True, nbEmpty + 1)
        else:
            if nbEmpty >= 1:
                out.write("\n")
            return (False, 0)

    def open(self, path, mode, mkdir=False):
        if mkdir:
            self.mkdir_if_needed(path)
        return open(path, mode)

    def mkdir_if_needed(self, filename):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else: raise
