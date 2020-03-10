Styles = {
  'p': {'class': 'text'},
  'title': {'class': 'title'},
  'h1': {'class': 'h1'},
  'h2': {'class': 'h2'},
  'h3': {'class': 'h3'},
}

class Text:

  Indent = '  '
  ParagraphPrefix = Indent
  BlockPrefix = Indent + Indent
  TitlePrefix = ''
  LenIndent = len(Indent)

  @staticmethod
  def wsSplit(line):
    lstripped = line.lstrip()
    i = len(line) - len(lstripped)
    return (line[:i], line[i:])

  @staticmethod
  def indentLevel(line):
    if line.startswith(Text.Indent):
      return 1 + Text.indentLevel(line[Text.LenIndent:])
    else:
      return 0

  @staticmethod
  def commonWsPrefix(stringList, ignoreEmpty=False):
    """ Finds a common prefix for the given list of strings. A list of strings
        If the list has less than two elements or there is no common prefix, this
        returns an empty string. This ignores empty lines.
    """
    # Ignore empty lines
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
