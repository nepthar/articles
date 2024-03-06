import sys
import logging

# Notes:
# To keep handlers simple, we enforce that they return arrays (or iterables)
# I alternatively considered having each handler have a "next" handler, and
# instead of returning results, it would call "next" for each result it created.
# I decied against this ultimately because I think it results in the absolute
# simplest handler/pipelines. (and it fucks with the stack)

class Handler:
  """ An abstraction for dealing with data in chunks. A handler is the class
      that goes into a Pipeline. Each handler operates on the data and optionally
      pushes additional data down the pipeline.

      The two man functions, handle and finish, must both return lists.
  """

  def handle(self, i) -> list:
    """ Handle a bit of incoming data.
        Return a list of resuts, which may be empty
    """
    raise NotImplementedError

  def finish(self) -> list:
    """ Any cleanup/finlization work that should happen when the stream is over
        Return a list of results, which may be empty
    """
    return []

  def spy(self, name=None):
    """ Return a handler that behaves like this one, except it prints out the
        input and results to STDERR or the specified file
    """
    return SpyHandler(self, name)

  def __str__(self):
    return self.__class__.__name__


class SpyHandler(Handler):
  """ Spies on the underlying handler by writing the inputs/ouputs to the given
      file descriptor. Does not change behavior.
  """
  def __init__(self, underlying, loggerName=None):
    self.prefix = str(underlying)
    self.underlying = underlying
    self.log = logging.getLogger(loggerName)

  def handle(self, i):
    ret = self.underlying.handle(i)
    self.log.debug('%s(%s) -> %s', self.prefix, i, ret)
    return ret

  def finish(self):
    ret = self.underlying.finish()
    self.log.debug('%s(finish) -> %s', self.prefix, ret)
    return ret

  def __str__(self):
    return f"Spy({self.underlying})"


class SimpleHandler(Handler):
  """ Makes a handler out of a simple function. If the function returns None,
      SimpleHandler returns an empty tuple. The function is defined as a class
      property or static method called `function`
  """
  def handle(self, i):
    ret = self.__class__.function(i)
    return () if ret is None else [ret]


class Pipeline(Handler):
  """ A pipeline is an ordered sequence of handlers. The pipeline accumulates
      results as it goes and makes them available via the results method.
  """

  def __init__(self, handlers=None):
    self.results = []
    self.handlers = handlers if handlers else list()

  def _on_data(self, data):
    """ Run the actual pipeline, optionally calling finish on handlers """
    finish = len(data) == 0

    for h in self.handlers:
      data = [o for i in data for o in h.handle(i)]
      if finish:
        data.extend(h.finish())

    return data

  def append(self, next_handler):
    self.handlers.append(next_handler)

  def handle(self, i):
    ret = self._on_data([i])
    self.results.extend(ret)
    return ret

  def finish(self):
    ret = self._on_data([])
    self.results.extend(ret)
    return ret

  def results(self):
    return self.accum

  def process(self, iterable):
    for item in iterable:
      self.handle(item)
    self.finish()
    return self.results
