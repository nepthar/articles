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
  prefix = Text.ParagraphPrefix
  spanner = ProseSpanner()

  def decode(self, frame):
    return [ParagraphElement([s]) for s in self.spanner.span(frame.lines, dict())]


class TitleDecoder(Decoder):
  prefix = Text.TitlePrefix
  spanner = ProseSpanner()

  def __init__(self, style=None):
    self.style = style if style else {}

  def decode(self, frame):
    spans = self.spanner.span(frame.lines, dict(self.style))

    # We must have exactly one span at this point for the title.
    if len(spans) != 1:
      return None

    return [HeadingElement(spans)]


class UnknownDecoder(Decoder):
  def canDecode(self, frame):
    return True

  def decode(self, frame):
    return UnknownElement(frame)


class BlockDecoder(Decoder):
  prefix = Text.BlockPrefix

  def __init__(self, blockKey, mkElement, spanner):
    self.new = mkElement
    self.blockKey = blockKey
    self.sp = spanner

  def decode(self, frame):
    if frame.lines:
      key, _, val = frame.lines[0].partition(': ')
      if key == self.blockKey:
        return self.decodeBlock(frame.lines[1:], val)
    return None

  def decodeBlock(self, blockLines, value):
    spans = self.sp.span(blockLines)
    if len(spans) != 1:
      return None

    elem = self.new(spans)
    elem.meta['subtype'] = value

    return [elem]


Decoder.DefaultStack = [
  TitleDecoder(),
  ParagraphDecoder(),
  BlockDecoder('footnote', FootnoteElement, Spanner.Prose),
  BlockDecoder('inline', InlineNoteElement, Spanner.Prose),
  BlockDecoder('fixed', FixedWidthBlockElement, Spanner.Fixed),
  BlockDecoder('code', CodeBlockElement, Spanner.Fixed),
  BlockDecoder('quote', BlockQuoteElement, Spanner.Fixed),
]

class FrameDeocder(PipelineElement):
  def __init__(self, decoders=Decoder.DefaultStack, unknown=UnknownDecoder()):
    self.decoders = decoders
    self.unknown = unknown

  def handle(self, frame):
    for decoder in self.decoders:
      elements = decoder.tryDecode(frame)
      if elements is not None:
        [self.next.handle(e) for e in elements]
        return

    unknown = self.unknown.decode(frame)
    self.next.handle(unknown)
