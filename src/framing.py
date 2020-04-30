from pipeline import PipelineElement
from text import Text
from enum import Enum


# kinds of lines and frames
class Kind(Enum):
  Title   = 'ttl'
  Body    = 'bdy'
  Comment = 'cmt'
  Block   = 'blk'
  Break   = 'brk'
  Empty   = 'emt'
  Unknown = 'unk'


class Line:

  Kinds = set(Kind)

  def __init__(self, kind, line):
    assert(kind in self.Kinds)
    self.kind = kind
    self.line = line

  def __str__(self):
    return f"{self.kind.value}: {self.line}"


class Frame:

  Kinds = set(
    Kind.Title, Kind.Body, Kind.Comment,
    Kind.Block, Kind.Break, Kind.Unknown
  )

  def __init__(self, kind, lines=None):
    assert(kind in self.Kinds)
    self.kind = kind
    self.lines = lines if lines else []

  def __str__(self):
    return f'Frame({self.kind.name}, nlines={len(self.lines)})'


class LineClasifier(PipelineElement):
  """ Classifies the type of line based on prefix. This info can later
      be used by the framer
  """

  Prefixes = (
    # Known correct prefixes
    (Kind.Block, Text.BlockPrefix),
    (Kind.Comment, Text.CmtPrefix + ' '),
    (Kind.Comment, Text.CmtPrefix),
    (Kind.Body, Text.BodyPrefix),
    (Kind.Control, Text.ControlPrefix),

    # Bad prefixes. These are typos.
    (Kind.Unknown, ' '),
    (Kind.Unknown, '\t')
  )

  InvalidFirstChars = set(' \t')

  EmptyLine = Line(Kind.Empty, '')

  def __init__(self):
    # Since we're doing prefix checks, these must be ordered longest
    # to shortest.
    withLengths = ((k, p, len(p)) for k, p in self.Prefixes)

    self.prefixList = tuple(
      sorted(withLengths, reverse=True, key=lambda x: x[2])
    )

  def handle(self, line):
    if line:
      for kind, prefix, lenPrefix in self.prefixList:
        if line.startswith(prefix):
          self.next.handle(Line(kind, line[lenPrefix:]))

      else:
        if line[0] in self.InvalidFirstChars:
          self.next.handle(Line(Kind.Unknown, line))

        else:
          self.next.handle(Line(Kind.Title, line))

    else:
      self.next.handle(self.EmptyLine)


class ClassificationFramer(PipelineElement):

  BreakEmptyLines = 2
  BreakFrame = Frame(Kind.Break, ['<Section Break>'])

  def __init__(self):
    self.accum = []
    self.emptyCount = 0
    self.currentKind = None

  def flush(self):
    lines = self.accum
    # Remove starting newlines
    while lines and lines[0] == '':
      lines.pop(0)

    # Remove ending newlines
    while lines and lines[-1] == '':
      lines.pop()

    if lines:
      self.next.handle(Frame(self.currentKind, lines))

    self.accum.clear()
    self.currentKind = None

  def handle(self, classified):
    if classified.kind is Kind.Empty:
      self.emptyCount += 1

      if self.emptyCount < self.BreakEmptyLines:
        if self.currentKind == Kind.Block:
          self.accum.append('')
        else:
          self.flush()

      elif self.emptyCount == self.BreakEmptyLines:
        self.flush()
        self.next.handle(self.BreakFrame)

      else: # self.emptyCount > self.BreakEmptyLines
        # Ignore extra empty lines
        pass

    else:
      self.emptyCount = 0

      if classified.kind is not self.currentKind:
        self.flush()
        self.currentKind = classified.kind

      self.accum.append(classified.line)
