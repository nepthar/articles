#!/usr/bin/env python3
import sys

from src.framing import *
from src.pipeline import *
from src.decoders import FrameDecoder


class RightStripCharacters(SimpleHandler):
  function = lambda x: x.rstrip('\r\n\t ')


class Whateverer(SimpleHandler):
  @staticmethod
  def handle(x):
    return x


handlers = [
  RightStripCharacters(),
  LineFramer(),
  FrameDecoder(),
]

result = Pipeline(handlers).process(sys.stdin)

for r in result:
  print(r.debug())
  print('')

