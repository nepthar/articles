from elements import Element


class BlockElement(Element):
  directive = 'block'

  def __init__(self, args, spans):
    """ All BlockElement subclasses must be created this way """
    raise NotImplementedError


class CodeElement(BlockElement):
  directive = 'code'

  def __init__(self, args, spans):
    self.lang = args[0] if len(args) > 1 else 'shell'
    self.spans = spans


class QuoteElement(BlockElement):
  directive = 'quote'

  def __init__(self, args, spans):
    self.author = 'Fake Author, right before his death in 4040'
    self.spans = spans


class FigureElement(BlockElement):
  directive = 'figure'

  def __init__(self, args, spans):
    self.url = args[0]
    self.meta = KeyValue.toDict([s.text for s in spans])
    self.caption = self.meta.get('caption')
    self.align = self.meta.get('align', 'center')


class AttnElement(BlockElement):
  directive = 'attn'

  def __init__(self, args, spans):
    self.level = args[0] if len(args) > 1 else 'note'
    self.spans = spans


class SidenoteElement(BlockElement):
  directive = 'note'

  def __init__(self, args, spans):
    self.anchor = args[0:1]
    self.spans = spans


class FootnoteElement(BlockElement):
  directive = 'footnote'

  def __init__(self, args, spans):
    self.anchor = args[0:1]
    self.spans = spans


class FixedTextElement(BlockElement):
  directive = 'fixed'

  def __init__(self, args, spans):
    self.spans = spans


class LinkTableElement(BlockElement):
  directive = 'links'

  def __init__(self, args, spans):
    ## TODO:
    ## Parse this:
    ## [1]: First/link.jpg
    ## [2]: second.link.wikipeida/org
    ## [apples]: John Wilson, et al. Journal of bullshit Oct 30303

    ## To this:
    ## {
    ##   '1': 'First/link.jpg',
    ##   '2': 'second.link.wikipeida/org',
    ##   'apples': 'John Wilson, et al. Journal of bullshit Oct 30303'
    ## }
    pass
