# I dunno shit that didn't fit anywhere elsete
import re
import sys
import logging


def spy(member_func, member=False):
  prefix = f"{member_func.__qualname__}"
  log = logging.getLogger()
  def wrapped(*args, **kwargs):
    result = member_func(*args, **kwargs)
    if True: #log.isEnabledFor(logging.DEBUG):
      argstr = f"{args[1:]}" if member else f"{args}"
      kwargstr = f", {kwargs}" if kwargs else ''
      print(f"{prefix}({argstr}{kwargstr}) -> {result}")
    return result
  return wrapped


def addIf(key, a, b):
  """ Add a[key] to b if a[key] exists """
  if key in a:
    b[key] = a[key]


def flatten(iterable):
  for i in iterable:
    yield from i


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

