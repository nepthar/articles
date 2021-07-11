from ..pipeline import Handler


class RawTextRenderer(Handler):
  """ Render the article as an article """

  def handle(self, article):
    print(article.meta['title'])
    print('')
    for e in article.body:
      print(e.fullText())
      print('')
