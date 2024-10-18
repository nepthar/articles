import html

from elements import *
from spans import Span
from pipeline import Handler
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

  HeaderTemplate = """
  <!DOCTYPE html>
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
  Code = '<code>{}</code>'
  Pre = '<pre>{}</pre>'
  Unknown = "<h3>Unknown Frame {kind}</h3><pre>{text}</pre>"
  FooterTemplate = "</html>"


  def __init__(self):
    self.parts = []
    self.sections = 0
    self.written = []

  def write(self, part):
    self.written.append(part)

  def spanText(self, spans):
    parts = []
    for s in spans:

      for style in s.style:
        parts.append(f'<{style}>')

      parts.append(s.text)

      for style in s.style:
        parts.append(f'</{s}>')

    return '\n'.join(parts)

  def renderBody(self, e: Element):
    k = e.tag

    text = html.escape(self.spanText(e.spans))

    if k == 'h1' or k == 'h2':
      self.write(self.Heading.format(lvl=e.level, id=e.pid, text=text))

    elif k == 'p':
      self.write(self.Paragraph.format(text))

    elif k in set(('q', 'mn', 'in', 'fn', 'note')):
      self.write(self.Quote.format(text))

    elif k == 'code':
      self.write(self.Code.format(text))

    elif k == 'pre' or k == 'block':
      self.write(self.Pre.format(text))

    else:
      self.write(self.Unknown.format(kind=k, text=text))

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
