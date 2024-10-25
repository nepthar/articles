from pipeline import Handler

class Element:
  """ An Element is the Articles representation of bits of a document.
      It typically mirrors HTML/CSS concepts - tags, for instance
  """
  tag = None
  PreviewLength = 8
  lines = []

  def __init__(self, spans, **kwargs):
    assert(isinstance(spans, list))
    self.spans = spans
    self.attrs = kwargs
    self.ids = []

  def preview(self):
    if not self.spans:
      return ''
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
  tag = 'break'
  lines = []
  def __init__(self, **kwargs):
    super().__init__([], **kwargs)


class InvalidElement(Element):
  tag = 'invalid'
  def __init__(self, spans, **kwargs):
    super().__init__(spans, **kwargs)
    self.exception = kwargs.get('exception')


class UnknownElement(Element):
  tag = 'unknown'


class BlockElement(Element):
  tag = 'block'
  def __init__(self, directive, args, spans, **kwargs):
    super().__init__(spans, **kwargs)
    self.directive = directive
    self.args = args


class FixedTextElement(Element):
  tag = 'pre'


class MetadataElement(Element):
  tag = 'metadata'
  def __init__(self, md):
    super().__init__([])
    self.attrs = md


class CommentElement(Element):
  tag = 'cmt'


class TitleElement(Element):
  def __init__(self, spans, level=1, **kwargs):
    super().__init__(spans, **kwargs)
    self.level = level

  @property
  def tag(self):
    return f"h{self.level}"

  def __str__(self):
    return f"TitleElement(lvl={self.level})"


class NotImplementedElement(Element):
  tag = 'future'


class ParagraphElement(Element):
  tag = 'p'


class ListElement(Element):
  tag = 'ulist'


class OrderedListElement(Element):
  tag = 'olist'


class IdentifyElements(Handler):
  # TODO: Maybe don't use?

  def __init__(self, prefix=''):
    self.prefix = ''
    self.counts = {} # TOOD: Defaultdict

  def handle(self, item):
    tag = item.tag
    count = self.counts.get(tag, 0)
    self.counts[tag] = count + 1
    item.pid = f"{self.prefix}{tag}-{count}"
    return [item]
