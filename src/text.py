

class Text:

  Indent = '  '
  BodyPrefix = Indent
  BlockPrefix = Indent + Indent
  TitlePrefix = ''
  CmtPrefix = BodyPrefix + '//'
  ControlPrefix = 'ctl: '
  BreakPrefix = BodyPrefix + '---'

  LenIndent = len(Indent)

  AnyIndent = '<Any>'


  @staticmethod
  def isSlug(string):
    return False


  @staticmethod
  def removeIndent(line, level):
    if level == 0:
      return line
    else:
      toRemove = Text.Indent * level
      if line.startswith(toRemove):
        return line[len(toRemove):]
      else:
        raise ValueError('Line not at indent level')

  @staticmethod
  def prefix(line):
    if not line:
      return Text.AnyIndent

    if line.startswith(Text.BlockPrefix):
      return Text.BlockPrefix

    if line.startswith(Text.BodyPrefix):
      return Text.BodyPrefix

    return Text.TitlePrefix

  @staticmethod
  def wsSplit(line):
    lstripped = line.lstrip()
    i = len(line) - len(lstripped)
    return (line[:i], line[i:])

  @staticmethod
  def indentLevel(line):
    if line is '':
      return -1

    counter = 0
    while line.startswith(Text.Indent):
      counter += 1
      line = line[Text.LenIndent:]

    return counter

  @staticmethod
  def commonWsPrefix(stringList, ignoreEmpty=False):
    """ Finds a common prefix for the given list of strings. A list of strings
        If the list has less than two elements or there is no common prefix, this
        returns an empty string. This ignores empty lines.
    """
    # Ignore empty lines if desired
    candidates = [l for l in stringList if l] if ignoreEmpty else stringList

    listLength = len(candidates)

    if listLength == 0:
      return ''

    elif listLength == 1:
      return Text.wsSplit(candidates[0])[0]

    else:
      shortest = candidates[0]
      for s in candidates:
        if len(s) < len(shortest):
          shortest = s

      prefix = Text.wsSplit(shortest)[0]

      if all(s.startswith(prefix) for s in candidates):
        return prefix
      else:
        return ''
