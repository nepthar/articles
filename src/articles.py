#!/usr/bin/env python3
# 1. All of the lines of the file are in an array  array
# 2. Comment lines are removed
# 3. Split into chunks on two consecutive newlines
# 4. Parsed that way.

import sys
import gc
import textwrap
from collections import Counter

from pipeline import *
from decoders import *
from debug import *

from renderers import *
from misc import *

gc.disable()


class IdentifyElements(PipelineElement):
  def __init__(self):
    self.cnt = Counter()

  def handle(self, elem):
    num = self.cnt[elem.kind]
    newId = f'{elem.kind}{num}'
    self.cnt[elem.kind] += 1
    elem.pid = newId

    if isinstance(elem, HeadingElement):
      elem.ids.append(elem.fullText())

    self.next.handle(elem)


class AnythingPrinter(PipelineElement):

  def handle(self, thing):
    print(thing)



# a = Accumulator()
elements = [
  IndentSegmenter(),
  #LinePrinter()
  WriteNewlinesOnFinish(),
  EmptyLineFramer(),
#  FrameDumper(),
  FrameDecoder(),
  RawTextRenderer(),
  AnythingPrinter()
]

Pipeline(elements).process(sys.stdin)
# print(m.metadata)

# print(a.accum)