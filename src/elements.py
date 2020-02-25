class Span:
  def __init__(self, text, style=dict()):
    self.text = text
    self.style = style

Span.Empty = Span('', {})


class Element:
  def ids(self):
    """ A list of slugs that uniquely(ish) identify this element """
    return []


class UnknownElement(Element)
  def __init__(self, frame):
    self.frame = frame


class ImageElement(element):
  def __init__(self, src, span):
    self.src = src
    self.span = span

  def alt(self):
    return self.span.text


class HeadingElement(Element):
  def __init__(self, level, span, sectionId=None):
    self.level = level
    self.span = span

  def ids(self):
    if self.sectionId:
      return (self.sectionId, self.span.text)
    else:
      return (self.span.text,)


class ParagraphElement(Element):
  def __init__(self, span):
    self.span = span


class FootnoteElement(Element):
  def __init__(self, span):
    self.span = span


class InlineNoteElement(Element):
  def __init__(self, span):
    self.span = span


class BlockQuoteElement(Element):
  def __init__(self, span):
    self.span = span


class FormattedTextElement(Element):
  def __init__(self, span, fmt='text'):
    self.span = span
    self.fmt = fmt
