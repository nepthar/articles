

class Serde:

  className = None

  def serialize(self, object):
    pass

  def deserialize(self, stream):
    pass


class SpanSerde(Serde):

  className = 'Span'

