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


class MetadataElement(Element):
  kind = 'metadata'
  def __init__(self, md):
    super().__init__([], **md)


class UnknownElement(Element):
  kind = 'unknown'
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
  kind = 'section'

  @property
  def level(self):
    return self.meta.get('level', '2')


class ParagraphElement(Element):
  kind = 'paragraph'


class FootnoteElement(Element):
  kind = 'footnote'


class InlineNoteElement(Element):
  kind = 'inline'


class BlockQuoteElement(Element):
  kind = 'quote'


class FixedWidthBlockElement(Element):
  kind = 'rawtext'


class CodeBlockElement(Element):
  kind = 'code'
