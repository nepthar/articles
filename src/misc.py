# I dunno shit that didn't fit anywhere elsete
import re
import sys


class KeyValue:

  # https://regexr.com
  KVRegex = re.compile(r'^([\w\.]+):( ?)(.*)$')

  @staticmethod
  def extract(line):
    ex = KeyValue.KVRegex.match(line)
    if ex:
      key, _, val = ex.groups()
      return (key, val)
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
  Where = sys.stderr

  @staticmethod
  def warn(msg, *args):
    if Enabled:
      if args:
        msg = msg.format(args)
      print(f"warn: {msg}", file=Where)

  @staticmethod
  def log(msg, *args):
    if Enabled:
      if args:
        msg = msg.format(args)
      print(msg, file=Where)

