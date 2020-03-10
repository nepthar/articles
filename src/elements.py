from spans import *

PreviewLength = 8

class Element:
  renderClass = None
  def __init__(self, spans, **kwargs):
    assert(isinstance(spans, list))
    self.spans = spans
    self.meta = kwargs

  def ids(self):
    """ A list of slugs that uniquely(ish) identify this element """
    return []

  def getClass(self):
    return self.renderClass

  @property
  def preview(self):
    if self.spans:
      return ""
    else:
      pv = self.spans[0][:PreviewLength]
      return f"{pv}..."

  def __str__(self):
    return f'{self.__class__.__name__}'


class UnknownElement(Element):
  renderClass = 'text'
  def __init__(self, frame):
    super().__init__([])
    self.frame = frame


class ImageElement(Element):
  def src(self):
    return self.meta['src']

  def alt(self):
    return self.span.text


class HeadingElement(Element):
  def getClass(self):
    lvl = self.meta.get('level', '0')
    return f'h{lvl}'


class ParagraphElement(Element):
  renderClass = 'text'


class FootnoteElement(Element):
  renderClass = 'footnote'


class InlineNoteElement(Element):
  renderClass = 'inline'


class BlockQuoteElement(Element):
  renderClass = 'quote'


class FixedWidthBlockElement(Element):
  renderClass = 'fixed'


class CodeBlockElement(Element):
  renderClass = 'code'


class Article:
  def __init__(self):
    self.meta = {}
    self.elements = []

  def append(self, element):
    self.elements.append(element)

