import json
import framing
import spans
from misc import Log


class DeserializeError(ValueError):
  pass

# Deserialization Validation Helpers
def is_int(s):
  try:
    return int(s)
  except ValueError as e:
    raise DeserializeError(f'Invalid Int {s}')

def is_float(s):
  try:
    return float(s)
  except ValueError as e:
    raise DeserializeError(f'Invalid float {s}')

def is_equal(s, test):
  if s == test:
    return s
  else:
    raise DeserializeError(f'{s} is not {test}')

def is_in(s, possibleValues):
  if s in possibleValues:
    return s
  else:
    raise DeserializeError(f'{s} not in {possibleValues}')

def is_json(s):
  try:
    return json.loads(s)
  except json.decoder.JSONDecodeError as e:
    raise DeserializeError('Not Json') from e

def is_type(s, klass):
  t = type(s)
  if t is klass:
    return s
  else:
    raise DeserializeError(f'Wrong type. {t} is not {klass}')

def is_listof(l, klass):
  if type(l) is not list:
    raise DeserializeError(f'Not list: {l}')

  for i in l:
    is_type(i, klass)
  return l


class Serde:
  Class = None

  def serialize(self, item):
    pass

  def deserialize(self, string):
    pass


class FrameSerde(Serde):
  """ Frame {kind} {level} [json array of lines] """
  Class = framing.Frame

  def serialize(self, frame):
    s = json.dumps(frame.lines)
    return f'Frame {frame.kind} {frame.level} {s}'

  def deserialize(self, frameString):
    (frame, kind, level, js) = frameString.split(maxsplit=3)

    is_equal(frame, 'Frame')
    is_in(kind, framing.Frame.Kinds)
    ilvl = is_int(level)
    lines = is_listof(is_json(js), str)

    return framing.Frame(kind, ilvl, lines)


class SpanSerde(Serde):
  """ Span {json encoded test} {json encoded style dict} """
  Class = spans.Span

  def serialize(self, span):
    text = json.dumps(span.text)
    style = json.dumps(span.style)

    return f'Span {text} {style}'

  def deserialize(self, string):
    (span, _, rest) = string.partition(' ')

    is_equal(span, 'Span')
    d = json.JSONDecoder()

    text = ''
    style = None

    try:
      (text, lastChar) = d.raw_decode(rest)
      style = d.decode(rest[lastChar:])
    except json.decoder.JSONDecodeError as e:
      raise DeserializeError('Failed to decode Span text or style')

    span = spans.Span(text)
    span.style = style

    return span

