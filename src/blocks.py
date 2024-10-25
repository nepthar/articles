from text import Span
from elements import BlockElement, FixedTextElement
from pipeline import Handler


class BlockProcessor:
  def process(self, args, spans):
    raise NotImplementedError


class QuoteProcessor(BlockProcessor):
  pass


class CodeProcessor(BlockProcessor):
  directive = 'code'

  def decodeBlock(self, lines, argString):
    e = CodeBlockElement(self.spanner.span(lines))
    e.lang = argString
    return (e,)


class FixedTextProcessor(BlockProcessor):
  directive = 'pre'

  def process(self, args, spans):

    return [FixedTextElement(spans)]


class BlockDirectiveHandler(Handler):
  """ Runs through the list of registered block handlers """

  def __init__(self, processors={}, fallback=FixedTextProcessor()):
    self.processors = processors
    self.fallback = fallback

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
