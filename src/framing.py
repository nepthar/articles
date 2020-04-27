from pipeline import PipelineElement
from text import Text


class Frame:

  Kinds = set(('text', 'section', 'unknown'))

  def __init__(self, kind, level=0, lines=None):
    assert(kind in self.Kinds)
    self.lines = lines if lines else []
    self.level = level
    self.kind = kind

  def __str__(self):
    parts = [self.kind]

    if self.level is not None:
      parts.append(f'level={self.level}')

    if self.lines:
      parts.append(f'lines={len(self.lines)}')

    partsStr = ', '.join(parts)
    return f'<frame {partsStr}>'


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
