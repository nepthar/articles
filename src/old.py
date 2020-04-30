# old.py - Old stuff I want to keep in a file instead of git history

class EmptyLineSegmenter(PipelineElement):
  """ Calls finish whenever there's two empty lines in a row """
  def __init__(self, limit=2):
    self.nlCount = 0
    self.limit = limit

  def handle(self, line):
    if line is '':
      self.nlCount += 1
    else:
      self.nlCount = 0

    if self.nlCount < self.limit:
      self.next.handle(line)

    elif self.nlCount == self.limit:
      self.finish()

class LinesFramer(PipelineElement):
  def __init__(self):
    self.accum = []
    self.count = 0

  def handle(self, line):
    self.accum.append(line)

  def finish(self):
    lines = self.accum
    while lines and lines[-1] == '':
      lines.pop()

    if lines:
      # Ignore empty lines when finding a common prefix
      prefix = Text.commonWsPrefix(lines, ignoreEmpty=True)
      if prefix:
        li = len(prefix)
        self.next.handle(Frame(self.count, [l[li:] for l in lines], prefix))
      else:
        self.next.handle(Frame(self.count, lines))

      self.count += 1
      self.next.finish()

    self.accum = []

class MetadataReader(PipelineElement):
  def __init__(self):
    self.metadata = {}
    self.done = False

  def handle(self, line):
    if self.done:
      self.next.handle(line)
    else:
      key, val = KeyValue.extract(line)
      if key:
        self.metadata[key] = val
      else:
        self.warn(f"Bad KV Pair: {line}")

  def finish(self):
    self.done = True
    self.next.finish()


class OldFrame:

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


class OldFramer(PipelineElement):
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
      self.next.handle(OldFrame('text', self.currentIndent, lines))

    self.currentIndent = -1
    self.accum = []

  def handle(self, line):
    if line is '':
      self.emptyLineCount += 1

      if self.emptyLineCount == self.SectionEmptyLines:
        self.flush()
        self.next.handle(OldFrame('section'))

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
