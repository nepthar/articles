from misc import *
from frames import *
import sys

Blockquote = '    '
Paragraph = '  '


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

  def warn(self, message):
    print(message, file=sys.stderr)

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
      if line is not '':
        key, x, val = line.partition(': ')
        if x is ': ':
          self.metadata[key] = val
        else:
          self.warn(f"Bad KV Pair: {line}")

  def finish(self):
    self.done = True
    self.next.finish()


class IndentSegmenter(PipelineElement):
  """ Calls finish whenever indent level changes.
  """

  Indent = '  '

  def __init__(self, maxLevels=2):
    self.curIndent = 0
    self.il = len(self.Indent)
    self.max = maxLevels

  def getLevel(self, line, i=0):
    if line.startswith(self.Indent) and i < self.max:
      return self.getLevel(line[self.il:], i + 1)
    else:
      return i

  def handle(self, line):
    if line is not '':
      i = self.getLevel(line)
      if i != self.curIndent:
        self.curIndent = i
        self.finish()
    self.next.handle(line)


class EmptyLineSegmenter(PipelineElement):

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


class SegmentSanity(PipelineElement):
  def __init__(self):
    self.segment = []

  def handle(self, line):
    self.segment.append(line)

  def finish(self):
    seg = self.segment
    while seg and self.segment[-1] == '':
      seg.pop()

    if seg:
      for s in seg:
        self.next.handle(s)
      self.next.finish()

    self.segment = []


class TextReflowHandler(PipelineElement):
  def __init__(self):
    self.accum = []

  def canReflow(self, line):
    if line is not '':
      return not (line is '' or line.startswith(Blockquote))

  def handle(self, line):
    if self.canReflow(line):
      self.accum.append(line)
    else:
      self.flush()
      self.next.handle(line)

  def flush(self):
    if self.accum:
      if len(self.accum) == 1:
        self.next.handle(self.accum[0])
      else:
        toReflow = [self.accum[0]]
        toReflow.extend(l.strip() for l in self.accum[1:])
        self.next.handle(' '.join(toReflow))
      self.accum.clear()

  def finish(self):
    self.flush()
    self.next.finish()


class LinePrinter(PipelineElement):
  def handle(self, line):
    print(line)

  def finish(self):
    print("")