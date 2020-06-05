from spans import *

# todo: Work on the preview code. Ugh.

class Element:
  """ An Element is the Articles representation of bits of a document.
      It typically mirrors HTML/CSS concepts - tags, for instance
  """
  tag = None
  attrs = None
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
  def props(self):
    p = { 'src': self.meta['src'] }
    if 'alt' in self.meta:
      p['alt'] = self.meta['alt']
    return p


class BreakElement(Element):
  tag = 'bk'


class HeadingElement(Element):
  @property
  def tag(self):
    return 'h' + self.meta.get('level', '3')


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
    if 'lang' in self.meta:
      p['lang'] = self.meta['lang']
    return p




class CommentElement(Element):
  tag = 'hidden'