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
