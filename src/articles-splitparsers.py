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

  def handle(self, chunk):
    for line in chunk:
      self.handleLine(line)

  def getIndent(self, line):
    if line is '':
      return None

    # Read the indentation up to the length of the string

    return '' if c == 0 else line[:c]

  def handleLine(self, line):
    i = self.getIndent(line)

    if line is '':
      pass

    else if self.current is None:
      self.current = i

    else if self.current == i:
     pass

    else:
      self.flush()
      self.current = i

    self.accum.append(line)


  def flush(self):
    if self.accum:
      next.handle(self.accum)
      self.accum = []


a = NewlineChunker()

for line in sys.stdin:
  a.handle(line.rstrip('\n \t'))

a.finish()



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
