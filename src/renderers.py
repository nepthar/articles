from pipeline import PipelineElement
import textwrap


# class Renderer(PipelineElement):
#   pass


# class ArticleRenderer(PipelineElement):




# class FakeMLRender(PipelineElement):



class RawTextRenderer(PipelineElement):
  """ Render the article as an article """

  def handle(self, element):
    lines = [
      element.__repr__(),
      element.fullText(),
      ''
    ]
    print('\n'.join(lines))


  def finish(self):
    pass



