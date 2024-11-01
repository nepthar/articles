
class ArticlesError(Exception):
  pass


class DecoderError(ArticlesError):
  pass


class PipelineError(ArticlesError):
  pass


class FramingError(ArticlesError):
  pass


