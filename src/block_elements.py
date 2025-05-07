from elements import Element, BlockElement as BaseBlockElement
import re
from misc import KeyValue


class BlockElement(BaseBlockElement):
  directive = 'block'

  def __init__(self, args, spans):
    super().__init__(spans)
    self.args = args


class CodeElement(BlockElement):
  directive = 'code'

  def __init__(self, args, spans):
    super().__init__(args, spans)
    self.lang = args[0] if args and len(args) > 0 else 'shell'


class QuoteElement(BlockElement):
  directive = 'quote'

  def __init__(self, args, spans):
    super().__init__(args, spans)
    self.author = args[0] if args and len(args) > 0 else None


class FigureElement(BlockElement):
  directive = 'figure'

  def __init__(self, args, spans):
    super().__init__(args, spans)
    self.url = args[0] if args and len(args) > 0 else None
    self.meta = {}
    
    # Extract metadata from spans if they contain key-value pairs
    for span in spans:
      if ':' in span.text:
        key, value = span.text.split(':', 1)
        self.meta[key.strip()] = value.strip()
    
    self.caption = self.meta.get('caption')
    self.align = self.meta.get('align', 'center')


class AttnElement(BlockElement):
  directive = 'attn'

  def __init__(self, args, spans):
    super().__init__(args, spans)
    self.level = args[0] if args and len(args) > 0 else 'note'


class SidenoteElement(BlockElement):
  directive = 'note'

  def __init__(self, args, spans):
    super().__init__(args, spans)
    self.anchor = args[0] if args and len(args) > 0 else None


class FootnoteElement(BlockElement):
  directive = 'footnote'

  def __init__(self, args, spans):
    super().__init__(args, spans)
    self.anchor = args[0] if args and len(args) > 0 else None


class FixedTextElement(BlockElement):
  directive = 'fixed'

  def __init__(self, args, spans):
    super().__init__(args, spans)


class LinkTableElement(BlockElement):
  directive = 'links'

  def __init__(self, args, spans):
    super().__init__(args, spans)
    self.links = {}
    
    # Parse link definitions
    link_pattern = re.compile(r'^\[([^\]]+)\]:\s*(.+)$')
    
    for span in spans:
      match = link_pattern.match(span.text)
      if match:
        key, url = match.groups()
        self.links[key] = url.strip()
