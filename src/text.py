from typing import NamedTuple


class Collector:
  """
    There are only two kinds of collectors: One that preserves line breaks
    and one that doesn't. I've called them "poetry" and "prose".

    Prose is designed to be "reflowed", that is adjust to the view width.
  """
  @staticmethod
  def collect(lines):
    raise NotImplementedError

class PoetryCollector(Collector):
  @staticmethod
  def collect(lines):
    """ Aggregate lines of text preserving line breaks """
    return [Span(x) for x in lines]


class ProseCollector(Collector):
  @staticmethod
  def collect(lines):
    """ Aggregate lines of text without preserving line breaks """
    result = []
    cur = []
    for line in lines:
      if line:
        cur.append(line)
      else:
        result.append(Span(' '.join(cur)))
        cur = []

    if cur:
      result.append(Span(' '.join(cur)))

    return result


class Style(NamedTuple):
  ident: str
  description: str

Styles = {s.ident: s for s in [
  Style('b', 'bold/emphasis'),
  Style('i', 'italic',),
  Style('u', 'underline'),
  Style('stk', 'strikethrough'),
  Style('c', 'css class'),
  Style('sub', 'subscript'),
  Style('sup', 'superscript'),
  Style('smcaps', 'small caps'),
  Style('var', 'inline variable or keyword'),
  Style('l', 'link')
]}

class Span:
  """A Span represents a bit of text with the same style or link"""
  def __init__(self, text, link=None, style=None):
    self.text = text
    self.style = style if style else []
    self.link = link

  def is_plain(self):
    return len(self.style) == 0 and self.link is None

  def is_empty(self):
    return len(self.text) == 0

  def preview(self):
    if len(self.text) < 16:
      return self.text
    else:
      return self.text[:16] + '...'

  def __repr__(self):
    return f'Span({self.preview()})'



class Stylizer:
  # The
  Priority = 100

  """ Takes a Span and generates a list of Spans, optionally styled """
  def apply(self, span):
    raise NotImplementedError


class NoopStyleizer:
  """ Does not style anything """
  def apply(self, span):
    return [span]

