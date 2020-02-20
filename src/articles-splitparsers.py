# 1. All of the lines of the file are in an array  array
# 2. Comment lines are removed
# 3. Split into chunks on two consecutive newlines
# 4. Parsed that way.

import sys
import pprint

import re
from nouns import *


rex = re.compile(r'\n{3,}')



class Accumulator:
  def __init__(self):
    self.stuff = []

  def handle(self, newSections):
    self.stuff.extend(newSections)


# Split on regex "\n{3,}"

def partitionSections(f):
  result = []
  for segment in re.split(rex, f.read(-1)):
    if segment:
      result.append(segment.split('\n'))

  return result


class NextSink:
  def __init__(self):
    self.count = 0
    self.chunks = []

  def handle(self, chunk):
    self.chunks.append(chunk)

  def finish(self):
    print("Finished chunks:")
    for i, c in enumerate(self.chunks):
      print(f"-- {i} --\n{c}")

Sink = NextSink()


class NewlineChunker:
  """ Issues a new chunk every time there's `chunkAt` consecutive empty
      lines. This also strips excessive empty lines, including at the
      beginning
  """

  def __init__(self, chunkAt=2, next=Sink):
    self.ec = 0
    self.accum = []
    self.chunkAt = chunkAt
    self.next = next

  def flush(self):
    lastFullIndex = len(self.accum) - self.ec
    if lastFullIndex > 0:
      self.next.handle(self.accum[:lastFullIndex])
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


class IndentationChunker:
  """ Takes a given chunk of lines and subdivies it based on indentation
      level.
  """

  def __init__(self, indentChars=' \t', next=Sink):
    self.current = None
    self.accum = []
    self.ics = indentChars
    self.next = next

  def handle(self, chunk):
    print(f'got chunk: {chunk}')
    for line in chunk:
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

    print(f"Line: {i}: {line}")

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
    print(f"flushing: {self.accum}")
    if self.accum:
      self.next.handle(self.accum)
      self.accum = []

  def finish(self):
    self.flush()
    self.next.finish()

a = IndentationChunker()
b = NewlineChunker(next=a)

for line in sys.stdin:
  b.handle(line.rstrip('\n \t'))

b.finish()



def printSections(sections):
  for i, s in enumerate(sections):
    text = '\n'.join(s)
    print(f"--- {i} ---\n{text}\n")




# for line in sys.stdin:
#   cs.handle(line.rstrip('\n'))

# cs.finish()

# printSections(a.stuff)

# pp = pprint.PrettyPrinter()

# pp.pprint(a.stuff)
