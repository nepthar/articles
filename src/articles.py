from collections import Counter

from elements import *
from pipeline import PipelineElement



class Article:
  def __init__(self):
    self.meta = {}
    self.body = []
    self.links = {}
    self.sections = []

  @property
  def title(self):
    return self.meta['title']


class ArticleBuilder(PipelineElement):

  def __init__(self):
    self.article = Article()
    self.idCounts = Counter()

  def addIDs(self, element):
    num = self.idCounts[element.kind]
    element.pid = f'{element.kind}{num}'
    self.idCounts[element.kind] += 1

    # Section - Use the text contents as an ID as well
    if element.kind == 'section':
      element.ids.append(element.fullText())


  def handle(self, element):

    self.addIDs(element)

    if isinstance(element, MetadataElement):
      self.article.meta = element.meta
    else:
      self.article.body.append(element)

  def finish(self):
    self.next.handle(self.article)
    return self.next.finish()

