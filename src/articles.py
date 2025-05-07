from collections import Counter

from pipeline import Handler
from elements import *
from text import NoopStyleizer

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
    return self.meta.get('article') or self.meta.get('title', 'Untitled Article')


class ArticleBuilder(Handler):

  def __init__(self, stylizer=None):
    self.preamble = []
    self.sections = []
    self.section = Section()
    self.md = {}
    self.stylizer = stylizer if stylizer is not None else NoopStyleizer()

  def handle(self, e):
    if isinstance(e, MetadataElement):
      self.md = e.attrs
    elif isinstance(e, BreakElement):
      self.finish_section()
    else:
      # Apply styling to the element's spans
      if hasattr(e, 'spans') and e.spans:
        styled_spans = []
        for span in e.spans:
          styled_spans.extend(self.stylizer.apply(span))
        e.spans = styled_spans
        
      # For list elements, apply styling to each item's spans
      if isinstance(e, ListElement) and hasattr(e, 'items'):
        for i, item_spans in enumerate(e.items):
          styled_item_spans = []
          for span in item_spans:
            styled_item_spans.extend(self.stylizer.apply(span))
          e.items[i] = styled_item_spans
          
      self.section.elements.append(e)
    return []

  def finish_section(self):
    if self.section and self.section.elements:
      # "Demote" subsections
      for e in self.section.elements[1:]:
        if isinstance(e, TitleElement):
          e.level = 2

      self.sections.append(self.section)
    self.section = Section()

  def finish(self):
    self.finish_section()
    return [Article(
      self.md, self.preamble, self.sections
    )]

