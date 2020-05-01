from spans import *

# todo: Work on the preview code. Ugh.

class Element:
  kind = None
  PreviewLength = 8

  @staticmethod
  def previewText(inThing):
    if not inThing:
      return '<empty>'

    if isinstance(inThing, str):
      if len(inThing) <= Element.PreviewLength:
        return inThing
      else:
        return inThing[:Element.PreviewLength] + '..'

    return Element.previewText(str(inThing))

  def __init__(self, spans, **kwargs):
    assert(isinstance(spans, list))
    self.spans = spans
    self.meta = kwargs
    self.ids = []
    self.pid = '-'

  def preview(self):
    if not self.spans:
      return "<empty>"
    else:
      pv = self.spans[0].text[:self.PreviewLength]
      return f"\"{pv}..\""

  def __str__(self):
    return f'{self.__class__.__name__}(id={self.pid} {self.preview()})'

  def __repr__(self):
    return f'<{self.__class__.__name__} {self.pid}>'

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


class BreakElement(Element):
  kind = 'bk'


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


class CommentElement(Element):
  kind = 'comment'