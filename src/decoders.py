# frame -> element

class FrameDecoder:
  types = set()

  def canDecode(self, frame):
    return type(frame) in types

  def decode(self, frame):
    assert(self.canDecode(frame))
    return self.elements(frame)

  def elements(self, frame):
    raise NotImplementedException()


class HeadingFrameEncoder(FrameDecoder):
  def elements(self, frame):
    pass


class ParagraphFrameEncoder(FrameDecoder):
  def elements(self, frame):
    pass


class BlockquoteFrameEncoder(FrameDecoder):
  def elements(self, frame):
    pass


class MetadataFrameEncoder(FrameDecoder):
  def elements(self, frame):
    pass
