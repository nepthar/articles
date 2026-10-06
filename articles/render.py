import html

from .elements import *
from .block_elements import *
from .text import Span
from .pipeline import Handler
import sys


class Renderer(Handler):
  pass

#   # Section decorations
#   def header(self, article):
#     pass

#   def footer(self, article):
#     pass

#   def pre_section(self, section):
#     pass

#   def post_section(self, section):
#     pass

#   def page_break(self, e):
#     pass

#   def footnote(self, e):
#     pass

#   # Unusual elements - errors, comments
#   def unknown(self, e):
#     """ An unknown or reserved future element """
#     pass

#   def invalid(self, e):
#     """ An element that failed to parse """
#     pass

#   def comment(self, e):
#     """ A comment left in the article """
#     pass

#   # Normal elements
#   def title(self, e):
#     pass

#   def paragraph(self, e):
#     pass

#   def o_list(self, e):
#     pass

#   def u_list(self, e):
#     pass

#   def span(self, span):
#     pass

#   def dispatch_body(self, e: Element):
#     match e:
#       case TitleElement:
#         return self.title(e)
#       case ParagraphElement:
#         return self.paragraph(e)
#       case OrderedListElement:
#         return self.o_list(e)
#       case


#   def dispatch_block(self, e: BlockElement):


#   def handle(self, article):
#     self.results = []
#     self.results.append()



class PythonRenderer(Renderer):

  HeaderTemplate = """
  # This should be python code
  """

  def __init__(self):
    self.parts = []
    self.sections = 0

class SimpleHTMLRenderer(Renderer):

  HeaderTemplate = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
  <link rel="stylesheet" href="tufte.css"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
</head>"""
  Heading = '<h{lvl} id="{id}">{text}</h{lvl}>'
  BeginSection = '<section>'
  EndSection = '</section>'
  Paragraph = '<p>{}</p>'
  Quote = '<blockquote><p>{}</p></blockquote>'
  Code = '<pre><code>{}</code></pre>'
  Pre = '<pre>{}</pre>'
  UnknownBlock = "<h3>Unknown Block Element: {kind}</h3><pre>{text}</pre>"
  Unknown = "<h3>Unknown Element: {kind}</h3><pre>{text}</pre>"
  FooterTemplate = "</html>"


  def __init__(self):
    self.parts = []
    self.sections = 0
    self.written = []

  def write(self, part):
    self.written.append(part)

  # Inline style -> HTML tag. Links ('l') are handled separately.
  StyleTags = {
    'b': 'strong',
    'i': 'em',
    'u': 'u',
    'stk': 's',
    'sub': 'sub',
    'sup': 'sup',
    'var': 'code',
  }

  def spanHtml(self, span):
    """ One span as HTML. The text is escaped; the tags are not. """
    text = html.escape(span.text)
    for style in span.style:
      if style == 'l':
        text = f'<a href="{html.escape(span.link or "", quote=True)}">{text}</a>'
      elif style in self.StyleTags:
        tag = self.StyleTags[style]
        text = f'<{tag}>{text}</{tag}>'
    return text

  def spanText(self, spans, sep=''):
    """ Join spans as HTML. Prose pieces join with no separator. Lines of
        a block join with a newline.
    """
    return sep.join(self.spanHtml(s) for s in spans)


  def renderBody(self, e: Element):
    text = self.spanText(e.spans)
    lines = self.spanText(e.spans, '\n')

    match e:
      case TitleElement():
        self.write(self.Heading.format(lvl=e.level, id=e.pid, text=text))
      case ParagraphElement():
        self.write(self.Paragraph.format(text))
      case QuoteElement():
        self.write(self.Quote.format(lines))
      case CodeElement():
        self.write(self.Code.format(lines))
      case FixedTextElement():
        self.write(self.Pre.format(lines))

      case CommentElement():
        # Comments are notes for the writer. They are not published.
        pass

      case ListElement():
        tag = 'ol' if e.ordered else 'ul'
        attrs = ''
        if e.ordered and e.order_type != '1':
          attrs += f' type="{e.order_type}"'
        if e.ordered and e.start != 1:
          attrs += f' start="{e.start}"'
        self.write(f'<{tag}{attrs}>')
        for item_spans in e.items:
          self.write(f'<li>{self.spanText(item_spans)}</li>')
        self.write(f'</{tag}>')

      case BlockElement():
        self.write(self.UnknownBlock.format(kind=e.directive, text=lines))

      case UnknownElement():
        self.write(self.Unknown.format(kind="Undecodeable", text=lines))

      case Element():
        kind = e.__class__.__name__
        self.write(self.Unknown.format(kind=kind, text=lines))

      case other:
        raise Exception(f"Got something that wasn't an element: {other}")



  def handle(self, article):
    headerString = self.HeaderTemplate.format(title=article.title)
    self.write(headerString)

    self.write("<body><article>")
    self.write(f"<h1>{article.title}</h1>")

    for sec in article.sections:
      self.write('<section>')
      for element in sec.elements:
        self.renderBody(element)
      self.write('</section>')

    self.write("</article></body></html>")

  def finish(self):
    return self.written
