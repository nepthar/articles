# I dunno shit that didn't fit anywhere elsete
import re

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



xx = [
  "1. Eat dinner",
  "1. Eat nachos",
  "1  Drive cars"
]
