from typing import NamedTuple
from misc import Log


class Style(NamedTuple):
  ident: str
  description: str


class Span:

  Styles = {s.ident: s for s in [
    Style('b', 'bold/emphasis'),
    Style('i', 'italic',),
    Style('ul', 'underline'),
    Style('strk', 'strikethrough'),
    Style('c', 'arbitrary css class'),
    Style('sub', 'subscript'),
    Style('sup', 'superscript'),
    Style('scaps', 'small caps'),
    Style('var', 'inline variable or keyword'),
    Style('l', 'link')
  ]}

  def __init__(self, text, **style):
    self.text = text
    self.style = style


Span.Empty = Span('')


class Spanner:
  pass

class ProseSpanner(Spanner):
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


class FixedSpanner(Spanner):
  def span(self, lines):
    return [Span('\n'.join(lines))]


Spanner.Default = FixedSpanner()
Spanner.Prose = ProseSpanner()
Spanner.Fixed = FixedSpanner()
