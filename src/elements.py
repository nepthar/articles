

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

  def debug(self):
    ret = [self.__str__()]
    ret.extend(f" |{s.text}" for s in self.spans)
    return '\n'.join(ret)


  def __str__(self):
    return f'{self.__class__.__name__}({self.preview()})'

  def __repr__(self):
    return f'<{self.__class__.__name__} {self.pid}>'

  def text(self):
    return ''.join(s.text for s in self.spans)


class BreakElement(Element):
  def __init__(self, kind, **kwargs):
    super().__init__([], **kwargs)
    self.kind = kind
    self.tag = f'break-{kind}'


class InvalidElement(Element):
  tag = 'invalid'
  def __init__(self, spans, **kwargs):
    super().__init__(spans, **kwargs)
    self.exception = kwargs.get('exception')


class UnknownElement(Element):
  tag = 'unknown'


class MetadataElement(Element):
  tag = 'metadata'
  def __init__(self, md):
    super().__init__([], **md)


class CommentElement(Element):
  tag = 'cmt'


class TitleElement(Element):
  def __init__(self, spans, level=1, **kwargs):
    super().__init__(spans, **kwargs)
    self.level = level

  @property
  def tag(self):
    return f"h{self.level}"


class NotImplementedElement(Element):
  tag = 'future'


class ParagraphElement(Element):
  tag = 'p'


class BlockElement(Element):
  tag = 'block'


class ListElement(Element):
  tag = 'list'
