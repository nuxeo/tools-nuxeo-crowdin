#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#
# Handles aggregation of messages* files from a given list of repositories

import string, sys

class Aggregate:
    """
    Represents an aggregated version of messages.
    """
    def __init__(self, targetpath, origpaths):
        self.targetpath = targetpath
        self.origpaths = origpaths

class MessagesManager:
    """
    Aggregates and splits message files according to given list of Aggregate objects.
    """
    def __init__(self, aggregates):
        self.aggregates = aggregates

    def aggregate(self):
        for aggregate in self.aggregates:
            if len(aggregate.origpaths) > 1:
                # aggregate content and copy to target file
                i = 0
                for origpath in aggregate.origpaths:
                    if i == 0:
                        self.writeAggregated(origpath, aggregate.targetpath, 'w')
                    else:
                        self.writeAggregated(origpath, aggregate.targetpath, 'a', start=False)
                    i += 1
            else:
                # just copy the content to target file
                self.writeAggregated(aggregate.origpaths[0], aggregate.targetpath, 'w')

    def writeAggregated(self, filepath, targetpath, mode, start=True):
        fi = open(filepath, 'r')
        fo = open(targetpath, mode)
        if not start:
            fo.write("\n\n")
        fo.write("## DO NOT EDIT FOLLOWING LINE\n")
        fo.write("# " + filepath + "\n")
        try:
            emptyLines = 0
            for line in fi:

                if not line.rstrip():
                    emptyLines += 1
                    continue
                else:
                    if emptyLines >= 1:
                        fo.write("\n")
                    emptyLines = 0

                fo.write(line)

        finally:
            fi.close()
            fo.close()

    def split(self):
        for aggregate in self.aggregates:
            self.writeSplit(aggregate.targetpath, aggregate.origpaths)

    def writeSplit(self, filepath, targetpaths):
        if len(targetpaths) > 1:
            # just copy back content to target file, removing header
            fi = open(filepath, 'r')
            i = 0
            current = targetpaths[i]
            fo = None
            try:
                j = 0
                emptyLines = 0
                for line in fi:

                    if not line.rstrip():
                        emptyLines += 1
                        continue
                    else:
                        if emptyLines >= 1:
                            fo.write("\n")
                        emptyLines = 0

                    if "## DO NOT EDIT FOLLOWING LINE\n" == line:
                        # open next targetpath
                        if fo is not None:
                            fo.close()
                        current = targetpaths[i]
                        i += 1
                        fo = open(current, 'w')
                        j = 0
                        continue
                    elif (j == 0 or j == 1) and (line.startswith("# " + current)):
                        continue
                    elif emptyLines < 1:
                        fo.write(line)
                    j += 1
            finally:
                fi.close()
                if fo is not None:
                    fo.close()
        else:
            # just copy back content to target file, removing header
            fi = open(filepath, 'r')
            fo = open(targetpaths[0], 'w')
            try:
                i = 0
                emptyLines = 0
                for line in fi:

                    if not line.rstrip():
                        emptyLines += 1
                        continue
                    else:
                        if emptyLines >= 1:
                            fo.write("\n")
                        emptyLines = 0

                    if i == 0 and "## DO NOT EDIT FOLLOWING LINE\n" == line:
                        continue
                    elif (i == 0 or i == 1) and (line.startswith("# " + filepath)):
                        continue
                    elif emptyLines < 1:
                        fo.write(line)
                    i += 1
            finally:
                fi.close()
                fo.close()
