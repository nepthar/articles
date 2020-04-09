from text import *
from misc import Log
import sys


# TODO: This should go somewhere else, I think
class Frame:
  __slots__ = ('num', 'lines', 'prefix')
  def __init__(self, num, lines, prefix=''):
    assert(lines and lines[0]), "Empty frame"
    self.num = num
    self.lines = lines
    self.prefix = prefix

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return f'<Frame {self.num}, {len(self.lines)} lines>'


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

      return self.head.finish()
    else:
      raise Exception("Empty Pipeline")


class PipelineElement:
  next = None

  def name(self):
    return self.__class__.__name__

  def __repr__(self):
    return f'<{self.name()}>'

  def finish(self):
    return self.next.finish()


class EmptyLineFramer(PipelineElement):
  def __init__(self):
    self.emptyCount = 0
    self.currentIndent = 0
    self.accum = []

  def handle(self, line):
    if line is '':
      self.emptyCount += 1
    else:
      self.emptyCount = 0

    prefix = Text.prefix(line)










class IndentSegmenter(PipelineElement):
  """ Every time indent changes, make sure there's two consecutive
      newlines. Consider empty lines to belong to any indent level.
  """
  def __init__(self, maxLevels=2):
    self.curIndent = 0
    self.max = maxLevels
    self.prevEmpty = False

  def handle(self, line):
    if line is not '' and self.prevEmpty:
      i = min(Text.indentLevel(line), self.max)
      if i != self.curIndent:
        self.curIndent = i
        self.next.handle('')
        self.next.handle('')

    self.prevEmpty = line is ''
    self.next.handle(line)


class OldEmptyLineFramer(PipelineElement):

  def __init__(self, limit=2):
    self.emptyCount = 0
    self.frameCount = 0
    self.limit = limit
    self.accum = []

  def handle(self, line):
    if line is '':
      self.emptyCount += 1
    else:
      self.emptyCount = 0

    if self.emptyCount < self.limit:
      self.accum.append(line)

    elif self.emptyCount == self.limit:
      self.flushFrame()

  def flushFrame(self):
    lines = self.accum
    while lines and lines[-1] == '':
      lines.pop()

    if lines:
      prefix = Text.commonWsPrefix(lines, ignoreEmpty=True)
      if prefix:
        lp = len(prefix)
        self.next.handle(Frame(self.frameCount, [l[lp:] for l in lines], prefix))
      else:
        self.next.handle(Frame(self.frameCount, lines))

      self.frameCount += 1

    self.accum = []

  def finish(self):
    self.flushFrame()
    return self.next.finish()


# I could alternatively just have the Pipeline instance issue two empty
# newlines at the end of the file?
class WriteNewlinesOnFinish(PipelineElement):
  def handle(self, x):
    self.next.handle(x)

  def finish(self):
    self.next.handle('')
    self.next.handle('')
    return self.next.finish()
