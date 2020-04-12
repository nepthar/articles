from pipeline import PipelineElement
import textwrap

# class HtmlHeader:
#   Charset = 'utf-8'
#   Lang = 'en'

#   def __init__(self, title=None):
#     self.title = title
#     self.meta = {}
#     self.links = []
#     self.scripts = []

#   def link(where, type=None, rel=None):
#     raise NotImplementedError()

#   def meta(key, value):
#     self.meta.append({'name': key, 'content': value})

#   def script(url,



# class HtmlBuilder:

#   Lang = 'en'

#   def __init__(self, title):
#     self.meta = []
#     self.body = []
#     self.feets = []




class SimpleHTMLRenderer(PipelineElement):

  HeaderTemplate = """<!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>{title}</title>
  </head>"""

  FooterTemplate = "</html>"

  Heading = '<h{lvl} id={id}>{t}</h{lvl}>'
  Paragraph = '<p>{}</p>'
  Quote = '<blockquote>{}</blockquote>'
  Code = '<pre>{}</pre>'

  Unknown = "<h3>Unknown Frame {kind}</h3><pre>{text}</pre>"

  def __init__(self):
    self.parts = []
    self.sections = 0

  def spanText(self, spans):
    parts = []
    for s in spans:

      for style in s.style:
        parts.append(f'<{style}>')

      parts.append(s.text)

      for style in s.style:
        parts.append(f'</{s}>')

    return ''.join(parts)

  def renderBody(self, part):
    k = part.kind

    text = self.spanText(part.spans)

    if k == 'section':
      self.next.handle("</section>")
      self.next.handle("<section>")
      self.next.handle(self.Heading.format(lvl=part.level, id=part.pid, t=text))

    elif k == 'paragraph':
      self.next.handle(self.Paragraph.format(text))

    elif k == 'quote':
      self.next.handle(self.Quote.format(text))

    elif k == 'code':
      self.next.handle(self.Code.format(text))

    else:
      self.next.handle(self.Unknown.format(kind=k, text=text))

  def handle(self, article):
    headerString = self.HeaderTemplate.format(title=article.title)
    self.next.handle(headerString)

    self.next.handle("<body><article>")
    self.next.handle(f"<h1>{article.title}</h1>")

    self.next.handle("<section>")

    for b in article.body:
      self.renderBody(b)

    self.next.handle("</section></article></body></html>")

  def finish(self):
    self.next.finish()


class RawTextRenderer(PipelineElement):
  """ Render the article as an article """

  def handle(self, article):
    print(article.meta['title'])
    print('')
    for e in article.body:
      print(e.fullText())
      print('')


class ReturnArticle(PipelineElement):
  def __init__(self):
    self.a = None

  def handle(self, article):
    self.a = article

  def finish(self):
    return self.a

