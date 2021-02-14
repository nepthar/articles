from .pipeline import Handler
from .misc import spy

class Frame:
  # The prefixes, if any, that this frame may begin with
  Prefixes = []

  # The number of empty lines that may be present in this frame before
  # the frame terminates
  MaxEmptyLines = 0

  def __init__(self, prefix=None):
    self.finished = False
    self.lines = []
    self.prefix = prefix
    self.empty_count = 0

  def add(self, line):
    self.empty_count = 0 if line else self.empty_count + 1
    if self.prefix:
      line = line.removeprefix(self.prefix)
    self.lines.append(line)

  def belongs(self, line):
    """ Test whether or not this line belongs to this frame """
    if self.finished:
      return False

    if line:
      # nonempty line, prefix must match if it exists
      if self.prefix and not line.startswith(self.prefix):
        return False
    else:
      # empty line, must be under max empty lines
      if self.empty_count >= self.MaxEmptyLines:
        return False

    return True

  def finish(self):
    """ Signal that this frame is finished and return self if the frame
        should be used, or None if it should be ignored (see EmptyFrame).
    """
    self.finished = True
    if self.empty_count > 0:
      # Strip trailing empty whitespace
      self.lines = self.lines[:-self.empty_count]

    return self

  def __repr__(self):
    pfx = 'None' if self.prefix is None else f"'{self.prefix}'"
    return f"<{self.__class__.__name__} lines={len(self.lines)} prefix={pfx}>"

  def debug(self):
    ret = [self.__repr__()]
    ret.extend(f" |{l}" for l in self.lines)
    return '\n'.join(ret)


class EmptyFrame(Frame):
  """ A special kind of frame that consists only of empty lines """
  def __init__(self, start_count):
    super().__init__()
    self.empty_count = start_count

  def belongs(self, line):
    return not line

  def add(self, line):
    self.empty_count += 1

  def finish(self):
    """ This empty frame should be ignored unless it's more than one line """
    if self.empty_count > 1:
      self.lines = [''] * self.empty_count
      return self

  def __repr__(self):
    return f"<EmptyFrame lines={self.empty_count}>"


class UnknownFrame(Frame):
  """ An unknown frame will continue to accumulate until an empty line """
  pass


class InvalidFrame(Frame):
  Prefixes = ['\t', '  \t', ' ']


class CommentFrame(Frame):
  Prefixes = ['// ', '  // ']


class TitleFrame(Frame):
  Prefixes = ['']


class ParagraphFrame(Frame):
  Prefixes = ['  ']



class BlockFrame(Frame):
  Prefixes = ['    ']
  MaxEmptyLines = 4


class ListFrame(Frame):
  Prefixes = ['   ']
  MaxEmptyLines = 1


class LineFramer(Handler):
  """ A handler that takes text line by line and frames it """
  @staticmethod
  def prefix_map(frame_classes):
    """ Generate a list of prefix -> Frame class """
    ret = [(pfx, fc) for fc in frame_classes for pfx in fc.Prefixes]
    return sorted(ret, reverse=True, key=lambda x: len(x[0]))

  def __init__(self, frame_classes=None):
    fcs = frame_classes if frame_classes else Frame.__subclasses__()
    self.prefix_map = LineFramer.prefix_map(fcs)
    self.frame = EmptyFrame(0)
    self.empty_count = 0

  def handle(self, line):
    ret = None
    self.empty_count = self.empty_count + 1 if line else 0

    if not self.frame.belongs(line):
      ret = self.frame.finish()
      self.frame = self._nextFrame(line)

    self.frame.add(line)
    return [ret] if ret else []

  def finish(self):
    ret = self.frame.finish()
    return [ret] if ret else []

  def _nextFrame(self, line):
    if not line:
      # Empty count has already been incremented for this line, which
      # will be sent to the frame right away, so subtract one
      return EmptyFrame(self.empty_count - 1)

    for pfx, frame_class in self.prefix_map:
      if line.startswith(pfx):
        return frame_class(prefix=pfx)

    return UnknownFrame()
