u"""
materials submodule.
"""
from __future__ import absolute_import
import inspect

class Path(object):
    @staticmethod
    def materials():
        return(inspect.getfile(Path).split(u"__init__")[0])