

def commonPrefix(stringList):
  """ Finds a common prefix for the given list of strings. A list of strings
      If the list has less than two elements or there is no common prefix, this
      returns and empty string
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

class JournalParser:

  def __init__(self):
    self.emptyLine = 0
    self.items = []
    self.accum = []
    self.lc = 0

  def addText(self):
    # The paragraph is a block quote if it shares a common prefix
    prefix = commonPrefix(self.accum)
    if prefix == 0:
      self.addItem('p', text=' '.join(self.accum))
    else:
      prefixStr = self.accum[0][0:prefix]
      self.addItem('bq', lines=[l[prefix:] for l in self.accum], prefix=prefixStr)

  def addItem(self, kind, **meta):
    d = meta
    d['kind'] = kind
    self.items.append(d)
    self.emptyLine = 0
    self.accum.clear()

  def _parse_line(self, line):
    if line == '':
      self.emptyLine += 1
      if self.accum:
        self.addText()
      return

    if self.accum:
      self.accum.append(line)
      return

    matched = titleSubtitleRx.match(line)
    if matched:
      (t, st) = matched.groups()
      self.addItem('title', title=t.strip(), subtitle=st.strip())
      return

    matched = titleRx.match(line)
    if matched:
      self.addItem('title', title=matched.groups()[0].strip(), subtitle=None)
      return

    matched = headingRx.match(line)
    if matched:
      weight = self.emptyLine
      self.addItem('heading', title=matched.groups()[0].strip(), weight=weight)
      return

    # Begin accumulating
    self.accum.append(line)

  def parse(self, textBlob):
    split = textBlob.split('\n')
    for line in split:
      self.lc += 1
      self._parse_line(line.rstrip('\n'))

    return self.items


class HtmlRenderer:

  def __init__(self):
    pass

  def renderTitle(self, i):
    return "<h1>{title}</h1>".format(**i)

  def renderHeader(self, i):
    level = 4 - i['weight']
    return "<h{lvl}>{title}</h{lvl}>".format(lvl=level, title=i['title'])

  def renderParagraph(self, i):
    return "<p>{}</p>".format(i['text'])

  def renderBlockQuote(self, i):
    renderedBq = '\n'.join(i['prefix'] + l for l in i['lines'])
    return "<pre>\n{}\n</pre>".format(renderedBq)

  def renderItem(self, i):
    kind = i['kind']
    if kind == 'title':
      return self.renderTitle(i)

    if kind == 'p':
      return self.renderParagraph(i)

    if kind == 'heading':
      return self.renderHeader(i)

    if kind == 'bq':
      return self.renderBlockQuote(i)

    return ">?????"

  def render(self, items):
    return '\n'.join(self.renderItem(i) for i in items)


class LineSink:
  def __init__(self):
    self.count = 0

  def handle(self, line):
    self.count += 1

  def finish(self):
    pass

Sink = LineSink()

class EmptyLineChunker:

  def __init__(self, maxEmpty=2, next=Sink):
    self.ec = 0
    self.accum = []

  def handle(self, line):
    self.accum.append(line)

    if line is '':
      self.ec += 1

    else:
      if self.ec > self.maxEmpty:
        chunk = self.accum[:-self.ec]
        self.next.handle(chunk)
        self.accum = []

      self.ec = 0
