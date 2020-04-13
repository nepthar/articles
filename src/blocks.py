




class BlockDecoder:
  """ Simple block handling """
  def __init__(self, kind, mkElement, spanner):
    self.kind = kind
    self.new = mkElement
    self.sp = spanner

  def decodeBlock(self, blockLines, value):
    elems = []
    for span in self.sp.span(blockLines):
      elem = self.new([span])
      if value:
        elem.meta['subtype'] = value
      elems.append(elem)

    return elems

