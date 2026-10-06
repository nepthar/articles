from typing import NamedTuple
import re


"""
Collectors
There are only two kinds of collectors: One that preserves line breaks
and one that doesn't. I've called them "poetry" and "prose".

Prose is designed to be "reflowed", that is adjust to the view width.
"""

def collect_poetry(lines):
  """ Aggregate lines of text preserving line breaks """
  return [Span(x) for x in lines]

def collect_prose(lines):
    """ Aggregate lines of text without preserving line breaks """
    result = []
    cur = []
    for line in lines:
      if line:
        cur.append(line)
      else:
        result.append(Span(' '.join(cur), prose=True))
        cur = []

    if cur:
      result.append(Span(' '.join(cur), prose=True))

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
  """A Span represents a bit of text with the same style or link.
     A prose span comes from collect_prose and may get inline styling.
     Other spans (poetry, block lines) keep their text as written.
  """
  def __init__(self, text, link=None, style=None, prose=False):
    self.text = text
    self.style = style if style else []
    self.link = link
    self.prose = prose

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


class InlineMarkdownStyleizer(Stylizer):
  """ Handles inline markdown styling - bold, italic, strikethrough, code
      and links. Styles do not nest. Underscores inside a word (snake_case)
      are not styling.
  """

  # Alternatives are tried left to right at each position, so code comes
  # first: `**x**` stays as code.
  TOKEN = re.compile(
    r"`(?P<var>[^`]+?)`"
    r"|\[(?P<ltext>[^\]]+?)\]\((?P<lurl>[^)\s]+?)\)"
    r"|\*\*(?P<b>.+?)\*\*"
    r"|(?<!\w)__(?P<b2>.+?)__(?!\w)"
    r"|~~(?P<stk>.+?)~~"
    r"|\*(?P<i>[^*\s](?:.*?[^*\s])?)\*"
    r"|(?<!\w)_(?P<i2>[^_\s](?:.*?[^_\s])?)_(?!\w)"
  )

  Styles = {'var': 'var', 'b': 'b', 'b2': 'b', 'stk': 'stk', 'i': 'i', 'i2': 'i'}

  def apply(self, span):
    """ Split a plain prose span into a list of plain and styled spans """
    if not span.prose or not span.is_plain():
      return [span]

    text = span.text
    result = []
    last_end = 0

    for match in self.TOKEN.finditer(text):
      start, end = match.span()
      if start > last_end:
        result.append(Span(text[last_end:start], prose=True))

      if match.group('ltext') is not None:
        result.append(Span(match.group('ltext'), link=match.group('lurl'), style=['l'], prose=True))
      else:
        name = match.lastgroup
        result.append(Span(match.group(name), style=[self.Styles[name]], prose=True))

      last_end = end

    if not result:
      return [span]

    if last_end < len(text):
      result.append(Span(text[last_end:], prose=True))

    return result
