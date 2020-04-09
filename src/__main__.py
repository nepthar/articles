#!/usr/bin/env python3


import sys
import gc
import textwrap
from collections import Counter

from pipeline import *
from decoders import *
from debug import *
from renderers import *
from misc import *
from articles import *

gc.disable()


class AnythingPrinter(PipelineElement):

  def handle(self, thing):
    print(thing)

  def finish(self):
    pass


class Tail(PipelineElement):
  def handle(self, thing):
    pass

  def finish(self):
    print('Pipeline finished', file=sys.stderr)


# a = Accumulator()
elements = [
  IndentSegmenter(),
  #LinePrinter()
  WriteNewlinesOnFinish(),
  EmptyLineFramer(),
  FrameDumper(),
  # FrameDecoder(),
  # ArticleBuilder(),
  # SimpleHTMLRenderer(),
#  ReturnArticle()
  #ElementDumper(),
  AnythingPrinter(),
  Tail()
]

Pipeline(elements).process(sys.stdin)
# print(m.metadata)

# print(a.accum)