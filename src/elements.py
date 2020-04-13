from spans import *


class Element:
  kind = None
  PreviewLength = 8

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
      pv = self.spans[0].text[:self.PreviewLength]
      return f"\"{pv}..\""

  def __repr__(self):
    return f'{self.__class__.__name__} id={self.pid}'

  def __str__(self):
    s = self.__repr__()
    return f'<{s} {self.preview()}>'

  def fullText(self):
    return ''.join(s.text for s in self.spans)


class MetadataElement(Element):
  kind = 'md'

  def __init__(self, md):
    super().__init__([], **md)


class UnknownElement(Element):
  kind = 'unk'

  def __init__(self, spans, frame):
    super().__init__(spans)
    self.frame = frame


class ImageElement(Element):
  kind = 'img'

  def src(self):
    return self.meta['src']

  def alt(self):
    return self.span.text


class HeadingElement(Element):
  kind = 'h'

  @property
  def level(self):
    return self.meta.get('level', '2')


class ParagraphElement(Element):
  kind = 'p'


class FootnoteElement(Element):
  kind = 'fn'


class InlineNoteElement(Element):
  kind = 'in'


class MarginNoteElement(Element):
  kind = 'mn'


class BlockQuoteElement(Element):
  kind = 'q'


class FixedWidthBlockElement(Element):
  kind = 'pre'


class CodeBlockElement(Element):
  kind = 'code'

