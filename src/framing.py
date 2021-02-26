import re

from .pipeline import Handler
from .misc import spy, KeyValue


def match_prefix(prefix, line):
  """ Match line against a prefix, except the line must exactly match or
      match without whitespace after
  """

  lp = len(prefix)
  ll = len(line)

  if ll < lp:
    return False

  if ll == lp:
    return prefix == line

  if ll > lp and line.startswith(prefix):
    nc = line[lp:lp+1]
    return nc == '' or not nc.isspace()

  return False


class Frame:
  # The prefixes, if any, that this frame may begin with
  Prefixes = []

  # The number of empty lines that may be present in this frame before
  # the frame terminates
  MaxEmptyLines = 0

  WhitespaceCheck = re.compile(r"\s.*")

  def __init__(self, prefix=None):
    self.finished = False
    self.lines = []
    self.prefix = prefix
    self.plen = len(prefix) if prefix else 0
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
      # nonempty line
      if self.prefix is not None:
        return match_prefix(self.prefix, line)

    else:
      # empty line, must be under max empty lines
      if self.empty_count >= self.MaxEmptyLines:
        return False

    return True

  def _match_prefix(self, line):
    """ Line must start with the prefix and have no extra whitespace """
    if not line.startswith(prefix):
      return False

    return not Frame.WhitespaceCheck.match(line[self.lenp:])

  def finish(self):
    """ Signal that this frame is finished and return the frame to use
        (usally self) or None if it should be ignored (see EmptyFrame).
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


class InvalidFrame(Frame):
  """ An invalid frame will continue to accumulate until an empty line """
  pass


class MetadataFrame(Frame):
  """ A special frame containing metadata info for the article. This can
      only be the first frame at the top of the document and must follow
      the KeyValue format.
  """
  def belongs(self, line):
    return not self.finished and KeyValue.KVRegex.match(line)


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


class PossibleFrame(Frame):
  """ A backtracking frame is used when there is more than one possibility for
      the current frame. Right now, it's just used for the first frame as
      either metadata, a title, or empty space.
  """
  def __init__(self, potentials):
    self.frames = potentials
    self.frames.append(InvalidFrame())

  def belongs(self, line):
    frames_belongs = [f for f in self.frames if f.belongs(line)]
    if frames_belongs:
      self.frames = frames_belongs
      return True
    else:
      return False

  def add(self, line):
    for frame in self.frames:
      frame.add(line)

  def finish(self):
    return self.frames[0]


class LineFramer(Handler):
  """ A handler that takes text line by line and frames it """
  @staticmethod
  def prefix_map(frame_classes):
    """ Generate a list of prefix -> Frame class """
    ret = [(pfx, fc) for fc in frame_classes for pfx in fc.Prefixes]
    return sorted(ret, reverse=True, key=lambda x: len(x[0]))

  def __init__(self, frame_classes=None):
    # NB: The top of the article could be empty space, metadata, or a title frame
    #     So, we use the PossibleFrame to try them all and see which wins.
    fcs = frame_classes if frame_classes else Frame.__subclasses__()
    self.prefix_map = LineFramer.prefix_map(fcs)
    self.frame = PossibleFrame([EmptyFrame(0), MetadataFrame(), TitleFrame('')])
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
      if match_prefix(pfx, line):
        return frame_class(prefix=pfx)

    return InvalidFrame()
