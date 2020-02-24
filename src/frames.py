class Frame:
  text = ''

  def __str__(self):
    preview = self.text[:6] + '...' if len(self.text) > 6 else self.text
    return f"{self.__class__.__name__}(style={self.style}, text={preview})"


class RawFrame(Frame):
  def __init__(self, lines, prefix=''):
    self.prefix = prefix
    self.lines = lines

  def __str__(self):
    strlines = '\n'.join(f"{self.prefix}|{l}" for l in self.lines)
    return f"Raw Frame:\n{strlines}"


class UnknownFrame(Frame):
  def __init__(self, frame):
    self.frame = frame
    self.text = '\n'.join(frame.lines)


class HeadingFrame(Frame):
  def __init__(self, level, text):
    self.level = level
    self.text = text


class ParagraphFrame(Frame):
  def __init__(self, text):
    self.text = text


class BlockquoteFrame(Frame):
  def __init__(self, text):
    self.text = text


class MetadataFrame(Frame):
  text = ''
  def __init__(self, metadata):
    self.md = metadata
