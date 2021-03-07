
def collect_prose(lines):
  """ Aggregate lines of text without preserving linebreaks """
  result = []
  cur = []
  for line in lines:
    if line is '':
      result.append(' '.join(cur))
      cur = []
    else:
      cur.append(line)

  if cur:
    result.append(' '.join(cur))

  return result


class Decoder:
  """ This class converts a frame into zero or more elements. Decoders
      should be 1:N with frames - that is, each frame has exactly 1 decoder.
  """

  # The class that this decoder handles
  FrameClass = None

  def can_decode(self, frame):
    return isinstance(frame, self.FrameClass)

  def decode(self, frame):
    raise NotImplementedError

  def try_decode(self, frame):
    if self.can_decode(frame):
      result = self.decode(frame)
      if result is None:
        cn = self.__class__.__name__
        raise ValueError(f'{cn} claimed to be able to decode, but failed')
      return self.decode(frame)
    else:
      return None


class SimpleDecoder(Decoder):
  Prose = True

  def decode_lines(self, lines):
    raise NotImplementedError

  def decode(self, frame):
    lines = collect_prose(frame.lines) if self.Prose else frame.lines
    return [self.decode_lines(lines)]
