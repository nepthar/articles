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

from renderers import *

gc.disable()

m = MetadataReader()


class AnyPrinter(PipelineElement):
  def __init__(self):
    self.i = 0

  def handle(self, item):
    print(f"{item}")

  def finish(self):
    print("<flush>")


class ElementDumper(PipelineElement):
  def __init__(self):
    self.i = 0

  def spanString(self, span):
    unNewlined = span.text.replace('\n', '\\n')
    return f'  | {unNewlined}'


  def handle(self, elem):
    l = [f'--[ {self.i}: {elem.__class__.__name__} :: {elem.kind} ]--']
    l.extend(self.spanString(s) for s in elem.spans)
    l.append(f'--[ {self.i}: end ]--')
    l.append('\n')
    print('\n'.join(l))
    self.i += 1


  def finish(self):
    print("-- finish --")


class FrameDumper(PipelineElement):
  def __init__(self):
    self.i = 0

  def handle(self, frame):
    self.i += 1
    lines = '\n'.join(f" |{l}" for l in frame.lines)
    print(f"Frame {self.i}. Prefix: |{frame.prefix}|\n{lines}\n")

  def finish(self):
    print("<flush>")


class Accumulator(PipelineElement):
  def __init__(self):
    self.accum = []

  def handle(self, element):
    self.accum.append(element)

  def finish(self):
    pass

# class DeduceHeadingLevels(PipelineElement):
#   def __init__(self):
#     pass

#   def handle(self, elem):

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

    print(f"Elem: {elem}\n  pid: {newId}\n  others: {elem.ids}")
    self.next.handle(elem)






# class ArticleCreator(PipelineElement):
#   def __init__(self, metaReader):

a = Accumulator()
elements = [
  EmptyLineSegmenter(),
  IndentSegmenter(),
  m,
  LinesFramer(),
  FrameDecoder(),
#  FrameDumper()
#  ElementDumper(),
  IdentifyElements(), a
#  TerminalRenderer()
]

Pipeline(elements).process(sys.stdin)
print(m.metadata)

print(a.accum)