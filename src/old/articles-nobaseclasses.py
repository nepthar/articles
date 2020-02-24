#!/usr/bin/env python3

import re
import pprint
import sys

pp = pprint.PrettyPrinter()

INDENT = '  '
COMMENT = '//'
BLOCK = '    '

RightRemoval='\r\n \t'

# class Paragraph:
#   def __init__(self, text):
#     self.text = text


# class InlineQuote:
#   def __init__(self, text, level):
#     self.text = text
#     self.level = level


# class Footnote:
#   def __init__(self, text, number):
#     self.text = text
#     self.number = number


# class Heading:
#   def __init__(self, text, level):
#     self.text = text
#     self.level = level


# class TextAccum:
#   def __init__(self, text):
#     self.text = text

titleSubtitleRx = re.compile(r"^\W*---(.*)--(.*)---\W*$")
titleRx = re.compile(r"^\W*---(.*)---\W*$")
headingRx = re.compile(r"^\W*--(.*)--\W*$")


class NoParser:

  def __init__(self):
    self.done = True

  def canParse(self, line):
    return False

  def parse(self, line):
    return False

  def items(self):
    return []


class EmptyParser:
  def __init__(self):
    self.count = 0
    self.done = False

  def parse(self, line):
    if line == '':
      self.count += 1
      return True
    else:
      self.done = True
      return False

  def items(self):

    return [{"type": "empties", "count": self.count}]


class CommentParser:
  def __init__(self):
    self.comment = ''
    self.done = True

  def parse(self, line):
    if line.startswith(COMMENT):
      self.comment = line.lstrip(COMMENT)
      return True
    else:
      return False

  def items(self):
    return [{ 'type': 'comment', 'text': self.comment }]


class HeadingParser:
  def __init__(self):
    self.content = []
    self.done = False

  def parse(self, line):
    if line == '':
      self.done = True
      return True
    else:
      self.content.append(line)
      return True

  def items(self):
    return [{'type': 'heading', 'text': ' '.join(self.content) }]



class ParagraphParser:
  def __init__(self):
    self.content = []
    self.accum = []
    self.done = False

  def parse(self, line):
    if line == '':
      if self.accum:
        self.content.append('\n'.join(self.accum))
        self.accum.clear()
      else:
        self.done = True
      return True

    if line.startswith(BLOCK):
      return False

    if line.startswith(INDENT):
      self.accum.append(line[2:])
      return True

    return False

  def items(self):
    return [{ 'type': 'ps', 'content': self.content}]


class BlockParser:
  def __init__(self):
    self.content = []
    self.accum = []
    self.done = False

  def parse(self, line):
    if line == '':
      if self.accum:
        self.content.append('\n'.join(self.accum))
        self.accum.clear()
      else:
        self.done = True
      return True

    if not line.startswith(BLOCK):
      return False

    self.accum.append(line[4:])
    return True

  def items(self):
    return [{'type': 'block', 'content': self.content}]


class ArticleParser:
  def __init__(self):
    self.emptyCount = 0
    self.items = []
    self.accum = []
    self.lc = -1
    self.noParser = NoParser()
    self.parser = self.noParser

  def checkParser(self):
    if self.parser and self.parser.done():
      self.items.append(self.parser.item())
      self.parser = None

  def np(self, line):
    if line == '':
      return EmptyParser()

    if line.startswith(COMMENT):
      return CommentParser()

    if line.startswith(BLOCK):
      return BlockParser()

    if line.startswith(INDENT):
      return ParagraphParser()

    return HeadingParser()

  def newParser(self, line):
    new = self.np(line)
    print(f"New: {new} - {line}")
    return new

  # def _parse(self, line):
  #   parsedLine = self.parser.parser(line)
  #   if self.parser.done():
  #     self.items.extend(self.parser.items())
  #     self.parser = self.noParser

  def nextLine(self, line):
    self.lc += 1

    usedLine = self.parser.parse(line)

    if self.parser.done:
      self.items.extend(self.parser.items())
      self.parser = self.noParser

      if not usedLine:
        self.parser = self.newParser(line)
        self.parser.parse(line)

  def finish():
    self.parser.finish()
    self.checkParser()


a = ArticleParser()

for line in sys.stdin:

  a.nextLine(line.rstrip(RightRemoval))


for i in a.items:
  print(i)
  print("")