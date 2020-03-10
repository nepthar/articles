from pipeline import PipelineElement
from misc import *
from elements import *
from spans import *
from text import *


class Decoder:
  prefix = None
  spanner = None

  def canDecode(self, frame):
    return frame.prefix == self.prefix

  def decode(self, frame):
    return None

  def tryDecode(self, frame):
    if self.canDecode(frame):
      return self.decode(frame)
    else:
      return None


class ParagraphDecoder(Decoder):
  # TODO: Support for comments
  prefix = Text.ParagraphPrefix
  spanner = ProseSpanner()

  def decode(self, frame):
    paragraphs = []
    for s in self.spanner.span(frame.lines):
      paragraphs.append(ParagraphElement([s]))
    return paragraphs


class TitleDecoder(Decoder):
  prefix = Text.TitlePrefix
  spanner = ProseSpanner()

  def __init__(self, style=None):
    self.style = style if style else {}

  def decode(self, frame):
    spans = self.spanner.span(frame.lines)

    # We must have exactly one span at this point for the title.
    if len(spans) != 1:
      return None

    return [HeadingElement(spans)]


class UnknownDecoder(Decoder):
  spanner = Spanner.Fixed
  def canDecode(self, frame):
    return True

  def decode(self, frame):
    spans = self.spanner.span(frame.lines)
    return UnknownElement(spans, frame)


class SimpleBlockDecoder(Decoder):
  def __init__(self, mkElement, spanner):
    self.new = mkElement
    self.sp = spanner

  def decodeBlock(self, blockLines, value):
    elems = []
    for span in self.sp.span(blockLines):
      elem = self.new(spans)
      if value:
        elem.meta['subtype'] = value

    return elems

# todo

class UnlabeledBlockDecoder(Decoder):
  prefix = Text.BlockPrefix
  spanner = Spanner.Fixed

  def decode(self, frame):
    spans = self.spanner.span(frame.lines)
    return [BlockQuoteElement(spans)]




Decoder.DefaultStack = [
  TitleDecoder(),
  ParagraphDecoder(),
  BlockDecoder('footnote', FootnoteElement, Spanner.Prose),
  BlockDecoder('inline', InlineNoteElement, Spanner.Prose),
  BlockDecoder('fixed', FixedWidthBlockElement, Spanner.Fixed),
  BlockDecoder('code', CodeBlockElement, Spanner.Fixed),
  BlockDecoder('quote', BlockQuoteElement, Spanner.Fixed),
  UnlabeledBlockDecoder()
]

BlockDecoders = {
  'footnote': BlockDecoders(FootnoteElement, Spanner.Prose),
  'inline': BlockDecoder(InlineNoteElement, Spanner.Prose),
  'fixed': BlockDecoder(FixedWidthBlockElement, Spanner.Fixed),
  'code': BlockDecoder(CodeBlockElement, Spanner.Fixed),
  'quote': BlockDecoder(BlockQuoteElement, Spanner.Fixed),
  'default': BlockDecoder(BlockQuoteElement, Spanner.Fixed)
}

class FrameDeocder(PipelineElement):
  UnknownDecoder = UnknownDecoder()

  def __init__(self, decoders=Decoder.DefaultStack):
    self.decoders = decoders
    self.unknown = unknown

  def handle(self, frame):



    for decoder in self.decoders:
      elements = decoder.tryDecode(frame)
      if elements is not None:
        for e in elements:
          self.next.handle(e)
        return
    self.warn("Unable to decode frame")
    self.next.handle(self.UnknownDecoder.decode(frame))

