#!/usr/bin/env python3
import sys
import gc
import textwrap
from collections import Counter

from pipeline import *
from decoders import *
from debug import *
#from render import *
from misc import *
from articles import *

from serde import *
from framing import *

import config


# Command line tool. Who cares.
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


#dc = Default.decoderConfig()


elements = [
  LineClasifier(),
  ClassificationFramer(),
  #FrameDumper(),
  FrameDecoder(config.Default.decoderConfig()),
#  FrameSer()
  AnythingPrinter(),

  Tail()
]

Pipeline(elements).process(sys.stdin)
