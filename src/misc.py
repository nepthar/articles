# I dunno shit that didn't fit anywhere elsete
import re
import sys


class KeyValue:
  """
  Simple Key<>Value pairs with strict rules
  1. Keys must be \w chars or a period
  2. Values can't contain newline characters and must be present
  3. Format is key: value. The ': ' is specifically looked for
  """

  # https://regexr.com
  KVRegex = re.compile(r'^([\w\.]+): (.*)$')

  @staticmethod
  def extract(line):
    ex = KeyValue.KVRegex.match(line)
    if ex:
      return ex.groups()
    else:
      return (None, None)


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

