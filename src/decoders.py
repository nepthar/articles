


class Decoder:
  """ Decodes a Frame to one or more elements """
  kind = None
  spanner = None

  def canDecode(self, frame):
    return frame.kind == self.kind

  def decode(self, frame):
    return None

  def tryDecode(self, frame):
    if self.canDecode(frame):
      result = self.decode(frame)
      if result is None:
        cn = self.__class__.__name__
        raise ValueError(f'{cn} claimed to be able to decode, but failed')
      return self.decode(frame)
    else:
      return None


class MetadataDecoder(Decoder):
  kind = Kind.Title

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
  noParagraphChar = '.'
  kind = Kind.Body
  spanner = ProseSpanner()

  def decode(self, frame):
    lines = frame.lines
    if len(lines) == 1 and lines[0] == self.noParagraphChar:
      return ()
    else:
      return [ParagraphElement(self.spanner.span(lines))]


class CommentDecoder(Decoder):
  kind = Kind.Comment
  spanner = ProseSpanner()

  def decode(self, frame):
    return [CommentElement(self.spanner.span(frame.lines))]


class BreakDecoder(Decoder):
  kind = Kind.Break
  spanner = None
  Response = (BreakElement([]),)

  def decode(self, frame):
    return self.Response


class TitleDecoder(Decoder):
  kind = Kind.Title
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
  kind = Kind.Block

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
    key, argString = KeyValue.extract(frame.lines[0])
    if key and key in self.decodeMap:
      return self.decodeMap[key].decodeBlock(frame.lines[1:], argString)
    elif self.default:
      return self.default.decodeBlock(frame.lines, None)
    else:
      return None


class FrameDecoder(PipelineElement):
  """ Convert raw frames into document elements """
  def __init__(self, decoders):
    self.decoders = decoders

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
