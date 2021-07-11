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
    self.elements = []

  def __repr__(self):
    if self.elements:
      return f'<Section {self.elements[0].preview()}>'


class Article:
  def __init__(self):
    self.meta = {}
    self.body = []
    self.links = {}
    self.sections = []

  @property
  def title(self):
    return self.meta['title']


class ArticleBuilder(Handler):

  def __init__(self):
    self.article = Article()
    self.idCounts = Counter()
    self.section = Section()

  def applyElementRules(self, element):
    num = self.idCounts[element.kind]
    element.pid = f'{element.kind}{num}'
    self.idCounts[element.kind] += 1

    # Heading-specific stuff
    if element.kind == 'h':
      element.ids.append(element.fullText())

      if not self.section.elements:
        element.meta['level'] = '2'

  def newSection(self):
    if self.section.elements:
      self.article.sections.append(self.section)
      self.section = Section()

  def handle(self, element):
    self.applyElementRules(element)

    if isinstance(element, MetadataElement):
      self.article.meta = element.meta

    elif isinstance(element, BreakElement):
      self.newSection()

    else:
      self.section.elements.append(element)


  def finish(self):
    return self.article

