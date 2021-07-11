#!/usr/bin/env python3
import sys

from src.framing import *
from src.pipeline import *
from src.decoders import FrameDecoder
from src.articles import ArticleBuilder

class RightStripCharacters(SimpleHandler):
  function = lambda x: x.rstrip('\r\n\t ')


class Whateverer(SimpleHandler):
  @staticmethod
  def handle(x):
    return x

class AnythingPrinter(Handler):

  def handle(self, thing):
    print(thing)

  def finish(self):
    pass


class Tail(Handler):
  def handle(self, thing):
    pass

  def finish(self):
    print('Pipeline finished', file=sys.stderr)


in_handlers = [
  RightStripCharacters(),
  LineFramer().spy('line_framer'),
  FrameDecoder(),
  ArticleBuilder(),
]

# out_handlers = [
#   ArticleBuilder(),
#   SimpleHTMLRenderer(),
#   AnythingPrinter(),
#   Tail()
# ]


def test_thingy():

  result = Pipeline(in_handlers).process(sys.stdin)

  for r in result:
    print(r.debug())
    print('')


test_thingy()
# def test_other_thingy():