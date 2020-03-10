from spans import *

PreviewLength = 8

class Element:
  kind = None
  def __init__(self, spans, **kwargs):
    assert(isinstance(spans, list))
    self.spans = spans
    self.meta = kwargs
    self.ids = []
    self.pid = '-'

  def preview(self):
    if not self.spans:
      return ""
    else:
      pv = self.spans[0].text[:PreviewLength]
      return f"\"{pv}..\""

  def __repr__(self):
    return f'{self.__class__.__name__} id={self.pid}'

  def __str__(self):
    s = self.__repr__()
    return f'<{s} {self.preview()}>'

  def fullText(self):
    return ''.join(s.text for s in self.spans)


class UnknownElement(Element):
  kind = 'u'
  def __init__(self, spans, frame):
    self.spans = spans
    self.frame = frame


class ImageElement(Element):
  kind = 'img'
  def src(self):
    return self.meta['src']

  def alt(self):
    return self.span.text


class HeadingElement(Element):
  kind = 's'

  @property
  def level(self):
    return self.meta.get('level', '0')

class ParagraphElement(Element):
  kind = 'p'


class FootnoteElement(Element):
  kind = 'f'


class InlineNoteElement(Element):
  kind = 'i'


class BlockQuoteElement(Element):
  kind = 'q'


class FixedWidthBlockElement(Element):
  kind = 'r'


class CodeBlockElement(Element):
  kind = 'c'

