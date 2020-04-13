from pipeline import PipelineElement
import textwrap





class ReturnArticle(PipelineElement):
  def __init__(self):
    self.a = None

  def handle(self, article):
    self.a = article

  def finish(self):
    return self.a

