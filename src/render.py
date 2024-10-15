import html

from elements import Element
from spans import Span
from pipeline import Handler
import sys


class Renderer(Handler):
  pass

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

    return ''.join(parts)

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

    elif k == 'pre':
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
