from collections import Counter

from pipeline import Handler

"""
Decision: We have to figure out how to deal with new sections. Maybe I should
just pass them along to the renderer? Hm...
"""

"""
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>Tufte CSS</title>
    <link rel="stylesheet" href="tufte.css"/>
    <link rel="stylesheet" href="latex.css"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
  </head>
  <body>
    <article>
      <h1 id="the-title">The Title</h1>
      <p class="subtitle">The Subtitle</p>
      <secion>
        <p>First paragraph...</p>
        ...
      </section>
      <section>
        <h2 id="major-section">Major Section</h2>
        <p>Major Section Intro</p>
        <h3 id="major-section--minor-section">Minor Section</h3>
        <p>minor section content>
      </section>
    </article>
  </body>
</html>
"""

class Section:
  def __init__(self):
    self.title = None
    self.slug = None
    self.elements = []

  def __repr__(self):
    if self.elements:
      return f'<Section {self.elements[0].preview()}>'


class Article:
  def __init__(self, meta, preamble, sections):
    self.meta = meta
    self.preamble = preamble
    self.sections = sections

  @staticmethod
  def empty():
    return Article({},[],[])

  @property
  def title(self):
    return self.meta.get('title')


class ArticleBuilder(Handler):

  def __init__(self):
    self.preamble = []
    self.sections = []
    self.section = None
    self.md = {}

  def handle(e):
    if isinstance(e, MetadataElement):
      self.md = e.attrs
    elif isinstance(e, BreakElement):
      self.finish_secion()
    else:
      self.section.elements.append(e)

  def finish_secion(self):
    if self.section:
      self.sections.append(self.section)
    self.section = Section()

  def finish(self):
    self.finish_secion()
    return [Article(
      self.md, self.preamble, self.sections
    )]

