#!/usr/bin/env python3
import sys
import os
import argparse

from framing import *
from pipeline import *
from decoders import FrameDecoder
from elements import IdentifyElements, TitleElement, BreakElement, ListElement
from articles import ArticleBuilder
from render import *
from blocks import *
from debug import *
from list_decoder import *
from text import InlineMarkdownStyleizer

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


class FileWriter(Handler):
  def __init__(self, output_path):
    self.output_path = output_path
    self.content = []
    
  def handle(self, content):
    self.content.append(content)
    return []
    
  def finish(self):
    with open(self.output_path, 'w') as f:
      for line in self.content:
        f.write(str(line) + '\n')
    logger.info(f"Output written to {self.output_path}")
    return []


def create_pipeline(output_file=None):
  """Create the main processing pipeline"""
  handlers = [
    RightStripCharacters(),
    LineFramer(),
    FrameDecoder(decoders=[ListDecoder()]),
    BlockDirectiveHandler(),
    ArticleBuilder(stylizer=InlineMarkdownStyleizer()),
    IdentifyElements(),
    SimpleHTMLRenderer(),
  ]
  
  if output_file:
    handlers.append(FileWriter(output_file))
  else:
    handlers.append(StdoutPrinter())
    
  return Pipeline(handlers)


def main():
  parser = argparse.ArgumentParser(description='Process article files into HTML')
  parser.add_argument('input_file', help='Input article file')
  parser.add_argument('-o', '--output', help='Output HTML file')
  parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging')
  
  args = parser.parse_args()
  
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
  
  input_file = args.input_file
  
  if not os.path.exists(input_file):
    logger.error(f"Input file not found: {input_file}")
    return 1
  
  output_file = args.output
  if not output_file:
    # Default output file is the same name with .html extension
    output_file = os.path.splitext(input_file)[0] + '.html'
  
  pipeline = create_pipeline(output_file)
  
  with open(input_file) as file:
    result = pipeline.process(file)
  
  return 0


if __name__ == "__main__":
  sys.exit(main())
