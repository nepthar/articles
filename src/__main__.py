#!/usr/bin/env python3
import sys

from framing import *
from pipeline import *
from decoders import FrameDecoder
from elements import IdentifyElements, TitleElement, BreakElement, ListElement
from articles import ArticleBuilder
from render import *
from blocks import *
from debug import *
from list_decoder import *

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


class ItemClassFilter(Handler):
  def __init__(self, klass):
    self.klass = klass

  def handle(self, thing):
    if isinstance(thing, self.klass):
      return [thing]
    else:
      return []

  def finish(self):
    return []


in_handlers = Pipeline([
  RightStripCharacters(),
  LineFramer(),
  FrameDecoder(),
  BlockDirectiveHandler(),
  ArticleBuilder(),
  SimpleHTMLRenderer(),
  StdoutPrinter()
])


frametest = Pipeline([
  RightStripCharacters(),
  LineFramer(),
  FrameDecoder(decoders=[ListDecoder()]),
  BlockDirectiveHandler(),
  ArticleBuilder(),
  SimpleHTMLRenderer(),
  StdoutPrinter()
])

pipeline = in_handlers

with open(sys.argv[1]) as file:
  result = pipeline.process(file)
