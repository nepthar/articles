import json
import framing


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
    isType(i, klass)
  return l


class FrameSerde:

  Class = framing.Frame

  @staticmethod
  def serialize(frame):
    s = json.dumps(frame.lines)
    return f'Frame {frame.kind} {frame.level} {s}'

  @staticmethod
  def deserialize(self, frameString):
    (frame, kind, level, js) = frameString.split(maxsplit=3)

    is_equal(frame, 'Frame')
    is_in(kind, Frame.Kinds)
    ilvl = is_int(level)
    lines = is_list_of(isJson(js), str)

    return Frame(kind, ilvl, lines)

