from ..pipeline import PipelineElement


class RawTextRenderer(PipelineElement):
  """ Render the article as an article """

  def handle(self, article):
    print(article.meta['title'])
    print('')
    for e in article.body:
      print(e.fullText())
      print('')
