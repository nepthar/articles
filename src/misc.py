# I dunno shit that didn't fit anywhere elsete

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


def commonPrefix(stringList):
  """ Finds a common prefix for the given list of strings. A list of strings
      If the list has less than two elements or there is no common prefix, this
      returns an empty string
  """
  if len(stringList) < 2:
    return 0

  prefix = 0
  shortest = stringList[0]
  for s in stringList:
    if len(s) < len(shortest):
      shortest = s

  for i, c in enumerate(shortest):
    if not all(entry[i] == c for entry in stringList):
      break
    prefix = i + 1

  return prefix