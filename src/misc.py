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



xx = [
  "1. Eat dinner",
  "1. Eat nachos",
  "1  Drive cars"
]
