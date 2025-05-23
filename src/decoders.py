from text import collect_poetry, collect_prose
from elements import *
from framing import *
from pipeline import Handler

import re


class Decoder:
  """
  This class converts a frame into zero or more elements. Decoders
  should be 1:N with frames - that is, each frame has exactly 1 decoder.
  Without overriding `decode`, it provides a simple way with some sane
  defaults
  """

  FrameClass = None
  ElementClass = NotImplementedElement
  Collector = collect_poetry

  def mk_element(self, frame, spans):
    return self.ElementClass(spans)

  def decode(self, frame):
    # Collector otherwise tries call this with self as the first arg.
    spans = self.Collector.__func__(frame.lines)
    return [self.mk_element(frame, spans)]


class EmptyDecoder(Decoder):
  FrameClass = EmptyFrame

  def decode(self, frame):
    return [BreakElement(empty_count=frame.empty_count)]


class BreakDecoder(Decoder):
  FrameClass = BreakElement


class InvalidDecoder(Decoder):
  FrameClass = InvalidFrame
  ElementClass = InvalidElement


class MetadataDecoder(Decoder):
  FrameClass = MetadataFrame
  def decode(self, frame):
    d = {}
    for line in frame.lines:
      k, v = KeyValue.extract(line)
      if k:
        d[k] = v
    return [MetadataElement(d)]


class CommentDecoder(Decoder):
  FrameClass = CommentFrame
  ElementClass = CommentElement
  Collector = collect_prose


class TitleDecoder(Decoder):
  FrameClass = TitleFrame
  ElementClass = TitleElement


class ParagraphDecoder(Decoder):
  FrameClass = ParagraphFrame
  ElementClass = ParagraphElement
  Collector = collect_prose


class BlockDecoder(Decoder):
  FrameClass = BlockFrame
  DirectiveRegex = re.compile(r'^([\w]+):( (.*))?$')

  def decode(self, frame):
    spans = collect_poetry(frame.lines)
    directive = 'unknown'
    args = ()

    dmatch = self.DirectiveRegex.match(spans[0].text)
    if dmatch:
      (directive, _, args) = dmatch.groups()
      spans = spans[1:]

    be = BlockElement(directive, args, spans)
    return [be]


class ListDecoder(Decoder):
  FrameClass = ListFrame
  ElementClass = ListElement


class FrameDecoder(Handler):
  """ Convert raw frames into document elements """
  def __init__(self, decoders=None):
    if decoders is None:
      decs = [dClass() for dClass in Decoder.__subclasses__()]
    else:
      decs = decoders

    self.decoders = {d.FrameClass: d for d in decs}

  def handle(self, frame):
    # Dispatch based on frame
    dec = self.decoders.get(frame.__class__)

    # TODO: Try/Catch -> invalid frame

    if dec:
      return dec.decode(frame)
    else:
      return [UnknownElement(PoetryCollector.collect(frame.lines))]
