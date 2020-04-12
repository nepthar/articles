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

from serde import FrameSerde
from framing import DefaultFramer

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


class FrameSer(PipelineElement):
  def __init__(self):
    self.frames = []
    self.fs = FrameSerde()

  def handle(self, frame):
    self.frames.append(frame)


  def finish(self):
    print("<onfinish>")
    for i, f in enumerate(self.frames):
      print(f'{i}: {self.fs.serialize(f)}')




elements = [
  DefaultFramer(),
  FrameSer(),
  Tail()
]

Pipeline(elements).process(sys.stdin)
