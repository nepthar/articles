from text import Span, collect_prose
from elements import BlockElement, FixedTextElement
from block_elements import *
from pipeline import Handler


class BlockProcessor:
  directive = None
  
  def process(self, args, spans):
    raise NotImplementedError


class QuoteProcessor(BlockProcessor):
  directive = 'quote'
  
  def process(self, args, spans):
    author = args[0] if args else None
    return [QuoteElement(args, spans)]


class CodeProcessor(BlockProcessor):
  directive = 'code'

  def process(self, args, spans):
    lang = args[0] if args else 'shell'
    return [CodeElement(args, spans)]


class FixedTextProcessor(BlockProcessor):
  directive = 'pre'

  def process(self, args, spans):
    return [FixedTextElement(spans)]


class FigureProcessor(BlockProcessor):
  directive = 'img'
  
  def process(self, args, spans):
    if not args:
      return [InvalidElement([Span("Missing image URL")])]
    return [FigureElement(args, spans)]


class AttnProcessor(BlockProcessor):
  directive = 'attn'
  
  def process(self, args, spans):
    return [AttnElement(args, spans)]


class SidenoteProcessor(BlockProcessor):
  directive = 'note'
  
  def process(self, args, spans):
    return [SidenoteElement(args, spans)]


class FootnoteProcessor(BlockProcessor):
  directive = 'footnote'
  
  def process(self, args, spans):
    return [FootnoteElement(args, spans)]


class LinkTableProcessor(BlockProcessor):
  directive = 'links'
  
  def process(self, args, spans):
    return [LinkTableElement(args, spans)]


class BlockDirectiveHandler(Handler):
  """ Runs through the list of registered block handlers """

  def __init__(self, processors=None, fallback=None):
    self.processors = {} if processors is None else processors
    self.fallback = fallback if fallback is not None else FixedTextProcessor()
    
    # Register default processors
    default_processors = [
      QuoteProcessor(),
      CodeProcessor(),
      FixedTextProcessor(),
      FigureProcessor(),
      AttnProcessor(),
      SidenoteProcessor(),
      FootnoteProcessor(),
      LinkTableProcessor()
    ]
    
    for processor in default_processors:
      if processor.directive:
        self.register(processor)

  def register(self, processor):
    self.processors[processor.directive] = processor

  def handle(self, block_element):
    if isinstance(block_element, BlockElement):
      processor = self.processors.get(block_element.directive)

      if processor:
        return processor.process(block_element.args, block_element.spans)
      else:
        spans = [
          Span(f"unhandled - {block_element.directive}({block_element.args})")
        ]
        spans.extend(block_element.spans)

        return self.fallback.process([], spans)

    else:
      return [block_element]
