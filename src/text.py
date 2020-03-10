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
  def indentLevel(line):
    if line.startswith(Text.Indent):
      return 1 + Text.indentLevel(line[Text.LenIndent:])
    else:
      return 0

  @staticmethod
  def commonIndent(stringList):
    if len(stringList) == 0:
      return ''

    i0 = Text.indentLevel(stringList[0])
    shared = all(Text.indentLevel(s) == i0 for s in stringList)

    if shared:
      return Text.Indent * i0
    else:
      return ''


  @staticmethod
  def commonPrefix(stringList):
    """ Finds a common prefix for the given list of strings. A list of strings
        If the list has less than two elements or there is no common prefix, this
        returns an empty string
    """
    listLength = len(stringList)

    if listLength < 2:
      return ''

    else:
      prefix = 0
      shortest = stringList[0]
      for s in stringList:
        if len(s) < len(shortest):
          shortest = s

      for i, c in enumerate(shortest):
        if not all(entry[i] == c for entry in stringList):
          break
        prefix = i + 1

      return shortest[:prefix]