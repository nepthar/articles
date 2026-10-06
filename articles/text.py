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


class InlineMarkdownStyleizer(Stylizer):
  """ Handles inline markdown styling - bold, italic, strikethrough, code """
  
  # Define patterns for markdown-style formatting
  PATTERNS = [
    # Bold with double asterisks: **bold**
    (r'\*\*(.*?)\*\*', ['b']),
    # Italic with single asterisks: *italic*
    (r'\*(.*?)\*', ['i']),
    # Bold with double underscores: __bold__
    (r'__(.*?)__', ['b']),
    # Italic with single underscores: _italic_
    (r'_(.*?)_', ['i']),
    # Strikethrough with double tildes: ~~strikethrough~~
    (r'~~(.*?)~~', ['stk']),
    # Inline code with backticks: `code`
    (r'`(.*?)`', ['var']),
    # Links with markdown format: [text](url)
    (r'\[(.*?)\]\((.*?)\)', ['l']),
  ]
  
  def apply(self, span):
    """
    Apply markdown styling to a span, breaking it into multiple spans as needed.
    Returns a list of styled spans.
    """
    if span.is_plain() is False:
      # If the span already has styling, don't process it further
      return [span]
      
    text = span.text
    result = []
    last_end = 0
    
    # Process each pattern
    for pattern, styles in self.PATTERNS:
      # Find all matches for this pattern
      for match in re.finditer(pattern, text):
        start, end = match.span()
        
        # If there's text before this match, add it as a plain span
        if start > last_end:
            result.append(Span(text[last_end:start]))
        
        # Handle links specially
        if 'l' in styles and len(match.groups()) > 1:
            # For links, the first group is the text and the second is the URL
            result.append(Span(match.group(1), link=match.group(2), style=styles))
        else:
            # For other styles, apply the style to the content
            result.append(Span(match.group(1), style=styles))
        
        last_end = end
    
    # Add any remaining text
    if last_end < len(text):
        result.append(Span(text[last_end:]))
    
    # If no styling was applied, return the original span
    if not result:
        return [span]
    
    return result
