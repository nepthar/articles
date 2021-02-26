from spans import *

class Element:
  """ An Element is the Articles representation of bits of a document.
      It typically mirrors HTML/CSS concepts - tags, for instance
  """
  tag = None
  PreviewLength = 8
  attrs = {}

  @staticmethod
  def preview_text(inThing):
    if not inThing:
      return '<empty>'

    if isinstance(inThing, str):
      if len(inThing) <= Element.PreviewLength:
        return inThing
      else:
        return inThing[:Element.PreviewLength] + '..'

    return Element.preview_text(str(inThing))

  def __init__(self, spans, **kwargs):
    assert(isinstance(spans, list))
    self.spans = spans
    self.kwargs = kwargs
    self.ids = []
    self.pid = '-'

  def preview(self):
    if not self.spans:
      return "<empty>"
    else:
      pv = self.spans[0].text[:self.PreviewLength]
      return f"\"{pv}..\""

  def from_kw(self, *keys):
    d = {}
    for k in keys:
      if k in self.kwargs:
        d[k] = self.kwargs[k]

    return d

  def __str__(self):
    return f'{self.__class__.__name__}(id={self.pid} {self.preview()})'

  def __repr__(self):
    return f'<{self.__class__.__name__} {self.pid}>'

  def text(self):
    return ''.join(s.text for s in self.spans)


class MetadataElement(Element):
  tag = 'metadata'

  def __init__(self, md):
    super().__init__([], **md)


class UnknownElement(Element):
  tag = 'unknown'

  def __init__(self, spans, frame):
    super().__init__(spans)
    self.frame = frame


class ImageElement(Element):
  tag = 'img'

  @property
  def attrs(self):
    return self.from_kw('src', 'alt')


class BreakElement(Element):
  tag = 'bk'


class HeadingElement(Element):
  def __init__(self, spans, level, **kwargs):
    super().__init__(spans, **kwargs)
    self.level = level

  @property
  def tag(self):
    return f"h{self.level}"


class ParagraphElement(Element):
  tag = 'p'


class NoteElement(Element):
  tag = 'note'

  @property
  def props(self):
    return {
      'class': 'attn',
      'level': self.props.get('level', 'info')
    }


class FootnoteElement(Element):
  tag = 'note'
  props = { 'class': 'footer' }


class MarginNoteElement(Element):
  tag = 'note'
  props = { 'class': 'margin' }


class BlockQuoteElement(Element):
  tag = 'blockquote'


class FixedWidthBlockElement(Element):
  tag = 'pre'


class CodeBlockElement(Element):
  tag = 'pre'

  @property
  def props(self):
    p = { 'class': 'code' }
    if 'lang' in self.attrs:
      p['lang'] = self.attrs['lang']
    return p

class CommentElement(Element):
  tag = 'cmt'