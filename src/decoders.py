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


class MetadataDecoder(Decoder):
  def __init__(self):
    self.done = False

  def canDecode(self, frame):
    return not self.done

  def decode(self, frame):
    # Only attempt to decode the first frame seen
    self.done = True

    md = {}
    for line in frame.lines:
      k, v = KeyValue.extract(line)
      if not k:
        return None
      md[k] = v

    return [MetadataElement(md)]


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


class BlockDecodeDispatcher(Decoder):
  prefix = Text.BlockPrefix

  def __init__(self, decoders=None, default=None):
    if decoders is None:
      decoders = []

    self.decodeMap = { d.kind: d for d in decoders }
    if default:
      self.default = self.decodeMap[default]
    else:
      self.default = None

  def addDecoder(self, decoder):
    self.decodeMap[decoder.kind] = decoder

  def setDefault(self, default):
    self.default = self.decodeMap[default]

  def decode(self, frame):
    key, value = KeyValue.extract(frame.lines[0])
    if key and key in self.decodeMap:
      return self.decodeMap[key].decodeBlock(frame.lines[1:], value)
    elif self.default:
      return self.default.decodeBlock(frame.lines, value=None)
    else:
      return None


class DecoderConfig:
  def __init__(self, meta, title, paragraph, block, others=[]):
    self.metaDec = meta
    self.titleDec = title
    self.paragraphDec = paragraph
    self.blockDec = block
    self.others = others

  def decoders(self):
    decs = [self.metaDec, self.titleDec, self.paragraphDec, self.blockDec]
    decs.extend(self.others)
    return decs



class FrameDecoder(PipelineElement):
  """ Convert raw frames into document elements """
  def __init__(self, config):
    self.useConfig(config)

  def useConfig(self, config):
    self._config = config
    self.decoders = config.decoders()

  def addBlockDecoder(self, decoder):
    self._config.blockDec.addDecoder(decoder)

  def handle(self, frame):
    for decoder in self.decoders:
      elements = decoder.tryDecode(frame)
      if elements is not None:
        for e in elements:
          self.next.handle(e)
        return

    Log.warn("Unable to decode {}", frame)
    elem = UnknownElement(Spanner.Fixed.span(frame.lines),frame)
    self.next.handle(elem)

