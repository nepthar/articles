#!/usr/bin/env python3
import sys

from framing import *
from pipeline import *
from decoders import FrameDecoder
from elements import IdentifyElements, TitleElement, BreakElement
from articles import ArticleBuilder
from render import *

import logging

logging.basicConfig(level=logging.DEBUG)

class RightStripCharacters(SimpleHandler):
  function = lambda x: x.rstrip('\r\n\t ')


class DebugPrinter(SimpleHandler):
  function = lambda x: print(x.debug())


class StdoutPrinter(SimpleHandler):
  function = lambda x: print(x)


class ElementsPrinter(SimpleHandler):
  @staticmethod
  def function(element):
    print(f"{element.pid}: {element.attrs}")


in_handlers = [
  RightStripCharacters(),
  LineFramer(),
  FrameDecoder(),
  ArticleBuilder(),
  SimpleHTMLRenderer(),
  StdoutPrinter()
]


def test_thingy():
  with open(sys.argv[1]) as file:
    return Pipeline(in_handlers).process(file)


  # for r in result:
  #   print(r.debug())
  #   print('')


x = test_thingy()
