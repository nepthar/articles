import sys


class PipelineElement:
  next = None

  def name(self):
    return self.__class__.__name__

  def __repr__(self):
    return f'<{self.name()}>'

  def finish(self):
    return self.next.finish()


class OutputWriter(PipelineElement):
  next = None

  def __init__(self, file=sys.stdout):
    self.file = file

  def handle(self, item):
    print(item, file=self.file)

  def finish(self):
    return None


class Pipeline:

  RightStripChars = '\r\n\t '

  def __init__(self, elements=None):
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
        self.head.handle(line.rstrip(self.RightStripChars))

      return self.head.finish()
    else:
      raise Exception("Empty Pipeline")
