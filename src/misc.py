# I dunno shit that didn't fit anywhere elsete
import re
import sys


class KeyValue:
  """
  Key<>Value pairs with strict rules for simplicitiy.
  1. Keys must be \w(alphanumeric or underscore) chars or a period
  2. Values can't contain newline characters and must be present (for
     boolean things, use "key: true" or similar)
  3. Format is key: value. The ': ' is specifically looked for
  """

  # https://regexr.com
  KVRegex = re.compile(r'^([\w\.]+): (.*)$')

  Invalid = (None, None)

  @staticmethod
  def extract(line):
    ex = KeyValue.KVRegex.match(line)
    if ex:
      return ex.groups()
    else:
      return KeyValue.Invalid

  @staticmethod
  def toDict(lines):
    parsed = []

    for line in lines:
      result = KeyValue.extract(line)
      if result is KeyValue.Invalid:
        raise ValueError(f'Invalid KeyValue Line: "{line}"')
      parsed.append(result)

    d = {}
    for k, v in parsed:
      if k in d:
        raise ValueError(f'Defined twice: {k}')
      d[k] = v

    return d


def arraySplit(token, arr):
  splits = []
  current = []
  for a in arr:
    if a == token:
      splits.append(current)
      current = []
    else:
      current.append(a)
  return splits


class Log:

  Enabled = True
  Out = sys.stderr

  @staticmethod
  def warn(msg, *args):
    if Log.Enabled:
      if args:
        msg = msg.format(args)
      print(f"warn: {msg}", file=Log.Out)

  @staticmethod
  def log(msg, *args):
    if Log.Enabled:
      if args:
        msg = msg.format(args)
      print(msg, file=Log.Out)

