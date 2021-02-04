from .pipeline import Handler

def spy(member_func):
  prefix = 'spy' #f"{member_func.__qualname__}"
  def wrapped(*args, **kwargs):
    result = member_func(*args, **kwargs)
    print(f"{prefix}({args[1:]},{kwargs}) -> {result}")
    return result
  return wrapped


class Frame:

  # The prefixes, if any, that this frame may begin with
  Prefixes = []

  # Whether or not this frame contains any content
  NoContent = True

  # The number of empty lines that may be present in this frame before
  # the frame terminates
  MaxEmptyLines = 0

  # If a frame's lines contain 'prose', then whitespace, including
  # linebreaks, will be mashed together. If not, all linebreaks and
  # spaces will be preserved
  Prose = True

  def __init__(self, prefix=None):
    self.lines = []
    self.prefix = prefix
    self.finished = not self.NoContent
    self.empty_count = 0

  def add(self, line):
    self.empty_count = self.empty_count + 1 if len(line) == 0 else 0

    if self.prefix:
      line = line.removeprefix(self.prefix)
    self.lines.append(line)

  #@spy
  def belongs(self, line):
    """ Test whether or not this line belongs to this frame """
    if self.finished:
      return False

    if len(line) == 0:
      if self.empty_count >= self.MaxEmptyLines:
        return False

    elif self.prefix and not line.startswith(self.prefix):
      return False

    return True

  def finish(self):
    self.finished = True
    if self.empty_count > 0:
      self.lines = self.lines[:-self.empty_count]

    if self.Prose:
      self.content = [' '.join(self.lines)]
    else:
      self.content = self.lines
    return True


class EmptyFrame(Frame):
  NoContent = True

class UnknownFrame(Frame):
  Prose = False

class BreakFrame(Frame):
  NoContent = True

class InvalidFrame(Frame):
  Prefixes = ['\t', '  \t', ' ']
  Prose = False

class CommentFrame(Frame):
  Prefixes = ['// ', '  // ']

class TitleFrame(Frame):
  Prefixes = ['']

class ParagraphFrame(Frame):
  Prefixes = ['  ']

class BlockFrame(Frame):
  Prefixes = ['    ']
  MaxEmptyLines = 4
  Prose = False

class ListFrame(Frame):
  Prefixes = ['   ']
  MaxEmptyLines = 1
  Prose = False


class LineFramer(Handler):

  @staticmethod
  def prefix_map(frame_classes):
    """ Generate a list of prefix -> Frame class """
    ret = [(pfx, fc) for fc in frame_classes for pfx in fc.Prefixes]
    return sorted(ret, reverse=True, key=lambda x: len(x[0]))

  def __init__(self, frame_classes=None):
    fcs = frame_classes if frame_classes else Frame.__subclasses__()
    self.pm = LineFramer.prefix_map(fcs)
    self.frame = None

    for p, fc in self.pm:
      print(f" - >{p}<")

  def handle(self, line):
    ret = []
    if self.frame and self.frame.belongs(line):
      self.frame.add(line)
      return []

    if self.frame:
      self.frame.finish()
      ret = [self.frame]

    self.frame = self.next_frame(line)
    if self.frame:
      self.frame.add(line)

    return ret

  def finish(self):
    if self.frame:
      self.frame.finish()
      return [self.frame]

    return []

  def next_frame(self, line):
    if len(line) == 0:
      return None

    for pfx, frame_class in self.pm:
      if line.startswith(pfx):
        return frame_class(prefix=pfx)

    return UnknownFrame()
