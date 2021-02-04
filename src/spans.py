
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

class Span:

  def __init__(self, text, link=None, style=None):
    self.text = text
    self.style = style if style else []
    self.link = link

  def isPlain(self):
    return len(self.style) == 0 and self.link is None

  def isEmpty(self):
    return len(self.text) == 0

  def preview(self):
    if len(self.text) < 16:
      return self.text
    else:
      return self.text[:16] + '...'

  def __repr__(self):
    return f'Span({self.preview()})'


def collectProse(lines):
  """ Aggregate lines of text without preserving line breaks """
  result = []
  cur = []
  for line in lines:
    if line is '':
      result.append(Span(' '.join(cur)))
      cur = []
    else:
      cur.append(line)

  if cur:
    result.append(Span(' '.join(cur)))

  return result


def collectPoetry(lines):
  """ Aggregate lines of text preserving line breaks """
  return [Span(x) for x in lines]


class LinesSpanner:
  """ Runs lines of text through a list of spanners. Once a spanner
      has assigned either a style or a link to a span, it is not fed through
      the rest.
  """

  def __init__(self, textLinesCollector, spanners):
    self.collect = textLinesCollector
    self.spanners = spanners

  def spanLines(self, lines):
    spans = self.collect(lines)

    for spanner in self.spanners:
      newSpans = []
      for span in spans:
        if span.isPlain():
          newSpans.extend(spanner.span(span.text))
        else:
          newSpans.append(span)
      spans = newSpans

    return spans

  def withSpanner(self, spanner):
    spanners = self.spanners.copy()
    spanners.append(spanner)
    return LinesSpanner(self.collect, spanners)


class RegexMatchSpanner:
  """ Generate spans that match a given regex. For each instance of the match
      toSpan is invoked with the match as its argument. Each match is expected
      to result in a single span or None.

      This allows for matching against a general/more simple regex and then
      later rejecting.
  """
  regex = None
  toSpan = None

  def span(self, text):
    results = []
    cur = 0

    for match in re.finditer(self.regex, text):
      span = self.toSpan(match)

      if span is not None:
        (s, e) = match.span()

        if s != cur:
          results.append(Span(text[cur:s]))

        results.append(span)
        cur = e

    if cur != len(text):
      results.append(Span(text[cur:]))

    return results


class MuckdownSpanner(RegexMatchSpanner):
  """ Add markdown style stuff. A broken clock is right twice a day """

  DefaultStyleMap = {
    '*': 'b',
    '_': 'u',
    '/': 'i',
    '~': 'stk'
  }

  def __init__(self, styleMap=DefaultStyleMap):
    chars = ''.join(f'\\{k}' for k in styleMap.keys())
    self.regex = re.compile(
      f'([{chars}])' + f'([^{chars}]+?)' + r'(\1)')

  def toSpan(self, match):
    print(match.groups())
    return Span('!!' + match.groups()[0])


class SimpleLinkSpanner(RegexMatchSpanner):
  """ Match carrot links. The link slug must not start or end with whitespace,
      so it matches these possile situations:
      1. A single non-whitespasce character
      2. Non whitespace at the start and end, matching as few characters between
  """
  regex = re.compile(r'<(\S|\S.*?\S)>')

  def toSpan(self, match):
    print(match.groups())
    return Span('!!' + match.groups()[0])


class LongLinkStyleSpanner(RegexMatchSpanner):
  """ An unsophisticated regex to look for long form links and spans. Can have
      mismatches, which are reported by returning None. Should run before the
      SimpleLinkSpanner.
  """
  regex = re.compile(r"''.+?''[<{].+?[}>]")

  def toSpan(self, match):
    print(match.groups())
    return Span('!!' + match.groups()[0])


Span.Empty = Span('')
ProseSpanner = LinesSpanner(collectProse, [])
PoetrySpanner = LinesSpanner(collectPoetry, [])
