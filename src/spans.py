
import re

from typing import NamedTuple
from misc import Log, flatten



class Style(NamedTuple):
  ident: str
  description: str

# Styles = {s.ident: s for s in [
#   Style('b', 'bold/emphasis'),
#   Style('i', 'italic',),
#   Style('u', 'underline'),
#   Style('stk', 'strikethrough'),
#   Style('c', 'css class'),
#   Style('sub', 'subscript'),
#   Style('sup', 'superscript'),
#   Style('smcaps', 'small caps'),
#   Style('var', 'inline variable or keyword'),
#   Style('l', 'link')
# ]}

# TODO: Consider having the spans only contain a start, end, and style
class Span:

  def __init__(self, text, link=None, style=None):
    self.text = text
    self.style = style if style else []
    self.link = link

  def isPlain(self):
    if len(self.style) == 0 and self.link is None:
      return True
    else:
      return False



Span.Empty = Span('')

class TextSpanner:
  next = None

  def span(self, span):
    if span.isPlain():
      if self.next:
        results = []
        for s in self.spanText()
      results = []
      for s in self.spanText(span.text):
        results.extend()
    else:
      return [span]

  def spanText(self, text):
    pass

  def andThen(self, textSpanner):
    self.next = textSpanner


class Spanner:

  def __init__(self, textToSpans):

  def span(self, linesOrSpans):
    assert(isinstance(linesOrSpans), list)
    results = []
    for ls in linesOrSpans:
      if isinstance(ls, str):
        results.extend(self.spanText(ls))

      elif isinstance(ls, Span) and ls.isPlain():
        results.extend(self.spanText(ls.text))

      else:
        results.append(ls)
    return results

  def spanText(self, text):
    """ Decode `text` into a list of one or more Spans """
    raise NotImplementedError


class RegexSpanner:
  regex = None
  matchToSpan = None






class LinkStyleSpanner:
  """ Parse out Links and Styled Spans. For the URL group characters see:
      https://tools.ietf.org/html/rfc3986.

      SimpleURLGroup does not allow all URL characters. If a complicated
      URL needs to be specified, it should be done via the link table,
      not inline.
  """
  LinkGroup = r'([^\|\<]+)'
  SimpleURLGroup = r'([\w\-\.\_\:\/\?\#\@\%\!\$\+\,\;\=]+)'
  StyleChars = r'[\w ,.:\-\;]'

  SimpleLink = re.compile(r'<(' + LinkStyleSpanner.LinkGroup '+)>')
  SlugLink = re.compile(r'<(' + LinkGroup '+)|(' + SimpleURLGroup '')
  Styled =

  def span(self, lines):
    ra


class ProseCollector:
  """ Aggregates lines of text into one span, coalescing linebreaks """
  def span(self, lines):
    spans = []
    cur = []
    for line in lines:
      if line is '':
        spans.append(Span(' '.join(cur)))
        cur = []
      else:
        cur.append(line)

    if cur:
      spans.append(Span(' '.join(cur)))
    return spans


class PoetryCollector(Spanner):
  """ Aggregates lines of text into one span per line, preserving linebreaks """
  def span(self, lines):
    return [Span('\n'.join(lines))]


Spanner.Default = FixedSpanner()
Spanner.Prose = ProseSpanner()
Spanner.Fixed = FixedSpanner()

:escaped_left_carrot:
:escaped_right_carrot:
:escaped_pipe: