from misc import *

class Pipeline:

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
        self.head.handle(line)
      self.head.finish()
    else:
      raise Exception("Empty Pipeline")


class PipelineElement:
  next = None


class StripRightWhitespace(PipelineElement):

  def handle(self, line):
    self.next.handle(line.rstrip("\n \t"))

  def finish(self):
    self.next.finish()


class NewlineFramer(PipelineElement):
  """ Issues a new chunk every time there's `chunkAt` consecutive empty
      lines. This also strips excessive empty lines, including at the
      beginning
  """

  def __init__(self, chunkAt=2):
    self.ec = 0
    self.accum = []
    self.chunkAt = chunkAt

  def flush(self):
    lastFullIndex = len(self.accum) - self.ec
    if lastFullIndex > 0:
      actual = self.accum[:lastFullIndex]
      self.next.handle(RawFrame(actual))
    self.accum = []

  def handle(self, line):
    if line is '':
      self.ec += 1

    else:
      if self.ec >= self.chunkAt:
        self.flush()

      self.ec = 0

    self.accum.append(line)

  def finish(self):
    self.flush()
    self.next.finish()


class IndentFramer(PipelineElement):
  """ Takes a given frame of lines and subdivies it based on indentation
      level.
  """

  def __init__(self, indentChars=' \t'):
    self.current = None
    self.accum = []
    self.ics = indentChars
    self.next = None

  def stripLine(self, line):
    if self.current and line is not '':
      return line[len(self.current):]
    else:
      return line

  def handle(self, frame):
    for line in frame.lines:
      self.handleLine(line)
    self.flush()

  def getIndent(self, line):
    if line is '':
      return None

    # This returns an empty string if c == 0
    for i, c in enumerate(line):
      if c not in self.ics:
        return line[:i]

  def handleLine(self, line):
    # This is written so as to intentionally clarify all of the
    # different logic branches
    i = self.getIndent(line)

    # 1. An unindentetd line can belong to any level of indentation
    # 2. If no indendation has been set yet, it gets set
    # 3. If the current indentation is the indentation that is set,
    #    Continue the frame
    # 4. The indentation is different from perviously set, so flush the
    #    current accumulation of lines, and set the indentation.

    if line is '':
      pass

    elif self.current is None:
      self.current = i

    elif self.current == i:
     pass

    else:
      self.flush()
      self.current = i

    self.accum.append(line)

  def flush(self):
    if self.accum:

      # Remove trailing whitespace
      while self.accum[-1] is '':
        self.accum.pop()

      frame = RawFrame([self.stripLine(l) for l in self.accum], self.current)
      self.next.handle(frame)
      self.accum = []

  def finish(self):
    self.flush()
    self.next.finish()


class CommentFramer(PipelineElement):
  """ Removes comments from frames, making them their own frame """

  def __init__(self):
    self.cmtFrame = None
    self.regFrame = None
    self.cc = '//'

  def flushReg(self):
    if self.regFrame:
      self.next.handle(self.regFrame)
      self.regFrame = None

  def flushCmt(self):
    if self.cmtFrame:
      self.next.handle(self.cmtFrame)
      self.cmtFrame = None

  def handle(self, frame):
    for line in frame.lines:

      if line.startswith(self.cc):
        if self.cmtFrame is None:
          self.cmtFrame = RawFrame([], self.cc)

        stripped = line.replace(self.cc, '').strip()
        self.cmtFrame.lines.append(stripped)
        self.flushReg()

      else:
        if self.regFrame is None:
          self.regFrame = RawFrame([], frame.prefix)

        self.regFrame.lines.append(line)
        self.flushCmt()

    self.flushCmt()
    self.flushReg()

  def finish(self):
    self.next.finish()


class FrameDumper(PipelineElement):

  def __init__(self, next=None):
    self.next = next
    self.count = 0

  def handle(self, frame):
    self.count += 1
    print(f"Frame {self.count}")
    for line in frame.lines:
      print(f"{frame.prefix}|{line}")
    print('')
    self.next.handle(frame)

  def finish(self):
    print('Called Finish')
    self.next.finish()


class FrameDecoder(PipelineElement):

  def __init__(self):
    self.metadata = False

  def contactFrameText(self, textLines):
    return '\n'.join(textLines)

  def metadataFromLines(self, lines):
    mdict = {}
    for line in lines:
      key, sep, value = line.partition(": ")
      if sep != ': ':
        raise ValueError(f"Malformed metadata pair: {line}")
      else:
        mdict[key] = value
    return Metadata(mdict)


  def handle(self, frame):
    p = frame.prefix

    if p == '  ':
      paragraphs = arraySplit('', frame.lines)
      for pg in paragraphs:
        pgText = '\n'.join(pg)
        self.next.handle(Paragraph(pgText))

    elif p == '    ':
      self.next.handle(Blockquote('\n'.join(frame.lines)))

    elif p == '//':
      self.next.handle(Comment('\n'.join(frame.lines)))

    elif p == '':
      if self.gotMetadata:
        self.next.handle(Heading(0, '\n'.join(frame.lines)))
      else:
        self.next.handle(self.metadataFromLines(frame.lines))
        self.gotMetadata = True

    else:
      self.next.handle(Unknown(frame))

  def finish(self):
    self.gotMetadata = False
    self.next.finish()


class Accumulator(PipelineElement):

  def __init__(self):
    self.accum = []

  def handle(self, frame):
    self.accum.append(frame)

  def finish(self):
    pass

  def result(self):
    return self.accum


class Logger(PipelineElement):
  def __init__(self, outFile=sys.stdout):
    self.f = outFile

  def handle(self, item):
    print(item, file=self.f)
    self.next.handle(item)

  def finish(self):
    pass
