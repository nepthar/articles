#!/usr/bin/env python3
# 1. All of the lines of the file are in an array  array
# 2. Comment lines are removed
# 3. Split into chunks on two consecutive newlines
# 4. Parsed that way.

import sys
import gc
import textwrap

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
    l = [f'--[ {self.i}: {elem.__class__.__name__} :: {elem.getClass()} ]--']
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
    lines = '\n'.join(f"    |{frame.prefix}|{l}" for l in frame.lines)
    print(f"Frame {self.i}\n{lines}\n")

  def finish(self):
    print("<flush>")



elements = [
  EmptyLineSegmenter(),
  IndentSegmenter(),
  m,
  LinesFramer(),
#  FrameDeocder(),
  FrameDumper()
#  ElementDumper(),
#  TerminalRenderer()
]

Pipeline(elements).process(sys.stdin)
print(m.metadata)
