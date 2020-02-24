#!/usr/bin/env python3

import sys


ParagraphIdent = '  '
Comment = '//'
BlockIndent = '    '

RightRemoval='\r\n \t'

class BaseParser:
  def __init__(self, maxEmpty=2):
    self.done = False
    self.emptyCount = 0
    self.maxEmpty = maxEmpty

  def _canParse(self, line):
    raise NotImplementedError

  def _parse(self, line):
    raise NotImplementedError

  def items(self):
    raise NotImplementedError

  def canParse(self, line):
    if line == '':
      self.emptyCount += 1
      if self.emptyCount >= self.maxEmpty:
        self.done = True
    else:
      self.emptyCount = 0

    if self.done:
      return False

    if not self._canParse(line):
      self.done = True
      return False

    return True

  def parse(self, line):
    if self.done:
      raise AssertionError('Parse after done')

    if not self.canParse(line):
      raise AssertionError('Parse on unhandled line')

    return self._parse(line)


class EmptyParser(BaseParser):
  def __init__(self):
    super().__init__()
    self.count = 0

  def _canParse(self, line):
    return line == ''

  def _parse(self, line):
    self.count += 1

  def items(self):
    return [{"type": "empties", "count": self.count}]


class CommentParser(BaseParser):
  def __init__(self):
    super().__init__()
    self.comment = ''

  def _canParse(self, line):
    return line.startswith(Comment)

  def _parse(self, line):
    self.comment = line.lstrip(Comment)

  def items(self):
    return [{ 'type': 'comment', 'text': self.comment }]


class HeadingParser(BaseParser):
  def __init__(self):
    super().__init__()
    self.content = []

  def _canParse(self, line):
    return line == '' or (not line[0] == line.lstrip()[0])

  def parse(self, line):
    if line == '':
      self.done = True
    else:
      self.content.append(line)

  def items(self):
    return [{'type': 'heading', 'text': ' '.join(self.content) }]


class ParagraphParser(BaseParser):
  def __init__(self):
    super().__init__()
    self.content = []
    self.accum = []

  def _canParse(self, line):
    return line == '' or (line.startswith(ParagraphIdent) and not line.startswith(BlockIndent))

  def parse(self, line):
    if line == '':
      if self.accum:
        self.content.append(' '.join(self.accum))
        self.accum.clear()

    else:
      self.accum.append(line.strip())

  def items(self):
    while self.content[-1] == '':
      self.content.pop()
    return [{ 'type': 'ps', 'content': self.content}]


class BlockParser(BaseParser):
  def __init__(self):
    super().__init__()
    self.content = []

  def _canParse(self, line):
    return line == '' or line.startswith(BlockIndent)

  def parse(self, line):
    self.content.append(line.lstrip())

  def items(self):
    while self.content[-1] == '':
      self.content.pop()
    return [{'type': 'block', 'content': self.content}]


class ArticleParser:
  def __init__(self):
    self.emptyCount = 0
    self.items = []
    self.lc = -1
    self.parser = EmptyParser()

  def newParser(self, line):
    if line == '':
      return EmptyParser()

    if line.startswith(Comment):
      return CommentParser()

    if line.startswith(BlockIndent):
      return BlockParser()

    if line.startswith(ParagraphIdent):
      return ParagraphParser()

    return HeadingParser()

  def nextLine(self, line):
    self.lc += 1

    if not self.parser.canParse(line):
      self.items.extend(self.parser.items())
      self.parser = self.newParser(line)

    self.parser.parse(line)

  def finish():
    self.items.extend(self.parser.items())


a = ArticleParser()

for line in sys.stdin:
  a.nextLine(line.rstrip(RightRemoval))


for i in a.items:
  print(i)
  print("")