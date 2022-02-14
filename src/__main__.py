#!/usr/bin/env python3
import sys

from framing import *
from pipeline import *
from decoders import FrameDecoder

class RightStripCharacters(SimpleHandler):
  function = lambda x: x.rstrip('\r\n\t ')


in_handlers = [
  RightStripCharacters(),
  LineFramer().spy('line_framer'),
  FrameDecoder(),
# ArticleBuilder(),
#  AnythingPrinter(),
#  Tail()
]


def test_thingy():

  result = Pipeline(in_handlers).process(sys.stdin)

  for r in result:
    print(r.debug())
    print('')


test_thingy()
# def test_other_thingy():