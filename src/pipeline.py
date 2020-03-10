from misc import *
from text import *
import sys

Blockquote = '    '
Paragraph = '  '

class Frame:
  def __init__(self, lines, prefix=''):
    self.lines = lines
    self.prefix = prefix

  def __str__(self):
    if self.lines:
      return f"Frame({self.prefix}|{self.lines[0]})"

    return f"Frame(empty)"


class Pipeline:

  StripChars = '\r\n\t '

  def __init__(self, elements=[]):
    if elements:
      self.head = elements[0]
      self.tail = elements[0]
      for e in elements[1:]:
        self.append(e)
    else:
      self.head = None
      self.tail = None

  def append(self, nextElement):
    assert(isinstance(nextElement, PipelineElement))
    if self.head and self.tail:
      self.tail.next = nextElement
      self.tail = nextElement
    else:
      self.head = nextElement
      self.tail = nextElement

  def process(self, fileHandle):
    if self.head:
      for line in fileHandle:
        self.head.handle(line.rstrip(self.StripChars))
      self.head.finish()
    else:
      raise Exception("Empty Pipeline")


class PipelineElement:
  next = None
  simpleName = None

  def name(self):
    if self.simpleName:
      return self.simpleName
    else:
      return self.__class__.__name__

  def __repr__(self):
    return f'<{self.name()}>'

  def warn(self, message):
    print(f'{self.name()} warn: {message}', file=sys.stderr)

  def finish(self):
    self.next.finish()


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


class IndentSegmenter(PipelineElement):
  """ Calls finish whenever indent level changes, ignoring empty lines """
  def __init__(self, maxLevels=2):
    self.curIndent = 0
    self.max = maxLevels

  def handle(self, line):
    if line is not '':
      i = min(Text.indentLevel(line), self.max)
      if i != self.curIndent:
        self.curIndent = i
        self.finish()
    self.next.handle(line)


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
        self.next.handle(Frame([l[li:] for l in lines], prefix))
      else:
        self.next.handle(Frame(lines))

      self.next.finish()

    self.accum = []

