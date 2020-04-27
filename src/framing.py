from pipeline import PipelineElement
from text import Text
from enum import Enum


# Maybe use these instead?
class Kind(Enum):
  Title   = 'ttl'
  Body    = 'bdy'
  Comment = 'cmt'
  Block   = 'blk'
  Break   = 'brk'
  Control = 'ctl'
  Empty   = 'emt'
  Unknown = 'unk'


# class ClassifiedLine:
#   def __init__(self, kind, line):


# class LineClasifier(PipelineElement):

#   Kinds = set(Kind)

#   def __init__(self):
#     self.prefixMap = (
#       # 4 Characters
#       ('    ', Kind.Block),
#       ('  //', Kind.Comment),

#       # 3 Characters
#       ('   ', Kind.Unknown),
#       ('  \t', Kind.Unknown),

#       # 2 Characters
#       ('  ', Kind.Body),
#       (' \t', Kind.Unknown),

#       # 1 Character
#       ('\t', Kind.Unknown),
#       (' ', Kind.Unknown),
#     )

#   def handle(self, line):
#     if line:
#       for prefix, kind in self.prefixMap:
#         if line.startswith(prefix):
#           return ClassifiedLine(kind, line[len(prefix):])





class Frame:

  Kinds = set(Kind)

  def __init__(self, kind, level=-1, lines=None):
    #assert(kind in self.Kinds)
    self.lines = lines if lines else []
    self.kind = kind
    self.level = level

  def __str__(self):
    parts = [self.kind]

    if self.level is not None:
      parts.append(f'level={self.level}')

    if self.lines:
      parts.append(f'lines={len(self.lines)}')

    partsStr = ', '.join(parts)
    return f'<frame {partsStr}>'


class LineClassifier(PipelineElement):

  PrefixInfo = (
    (4, '    ', Kind.Block),
    (4, '  //', Kind.Comment),
    (3, '   ', Kind.Unknown),
    (2, '  ', Kind.Body),
    (1, ' ', Kind.Unknown),
  )

  @staticmethod
  def classifyAndStripPrefix(line):
    if line:
      for lgth, pfx, kind in LineClassifier.PrefixInfo:
        if line.startswith(pfx):
          return (kind, line[lgth:])

      if line[:1].isspace():
        return (Kind.Unknown, line)

      return (Kind.Title, line)

    else:
      return (Kind.Empty, line)

  def handle(self, line):
    self.next.handle(self.classifyAndStripPrefix(line))

  def finish(self):
    self.next.finish()


# class ClassifiedLineFramer(PipelineElement):

#   SectionEmptyLines = 2

#   def __init__(self):
#     self.accum = []
#     self.emptyCount = 0
#     self.currentKind = Kind.Empty

#   def flush(self):
#     lines = self.accum
#     while lines and lines[-1][0] == Kind.Empty:
#       lines.pop()

#     if lines:
#       frame = Frame(self.currentKind)
#       self.next.handle()

#   def handle(self, line):

class DefaultFramer(PipelineElement):
  """ The Framer is responsible for breaking up the document into frames
      Each frame carries the raw lines that make it up and the indent
      level.

      Two empty lines will generate a new section frame
  """

  MaxIndent = 2
  SectionEmptyLines = 2

  def __init__(self):
    self.accum = []
    self.emptyLineCount = 0
    self.currentIndent = 0


  def flush(self):
    lines = self.accum
    while lines and lines[-1] == '':
      lines.pop()

    if lines:
      self.next.handle(Frame('text', self.currentIndent, lines))

    self.currentIndent = -1
    self.accum = []

  def handle(self, line):
    if line is '':
      self.emptyLineCount += 1

      if self.emptyLineCount == self.SectionEmptyLines:
        self.flush()
        self.next.handle(Frame('section'))

      elif self.currentIndent is not self.MaxIndent:
        self.flush()

      else:
        self.accum.append('')

    else:
      self.emptyLineCount = 0
      indent = min(Text.indentLevel(line), self.MaxIndent)

      if indent is not self.currentIndent:
        self.flush()
        self.currentIndent = indent

      self.accum.append(Text.removeIndent(line, self.currentIndent))

  def finish(self):
    self.flush()
    self.next.finish()
