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



# a = Accumulator()
elements = [
  IndentSegmenter(),
  #LinePrinter()
  WriteNewlinesOnFinish(),
  EmptyLineFramer(),
  HTMLFrameDumper(),
  # FrameDecoder(),
  # ArticleBuilder(),
  # SimpleHTMLRenderer(),
#  ReturnArticle()
  #ElementDumper(),
  AnythingPrinter()
]

Pipeline(elements).process(sys.stdin)
# print(m.metadata)

# print(a.accum)