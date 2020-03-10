class Span:
  def __init__(self, text, parent=None, style=None):
    self.text = text
    self.st = style if style else dict()
    self.parent = parent

  def clearStyle(self):
    self.st.clear()

  def getStyle(self, key, default=None):
    if key in self.st:
      return self.st[key]
    elif self.parent:
      return self.parent.getStyle(key, default)
    else:
      return default

  def setStyle(self, key, value=''):
    self.st[key] = value


Span.Empty = Span('', parent=None, style={})


# class Spanners(Spanner):
#   def __init__(self, spanners):
#     self.spanners = spanners

#   def span(lines, style):
#     accum = []







  # def append(self, spanner):
  #   self.spanners.append(spanner)


class Spanner:
  pass


class ProseSpanner(Spanner):
  def span(self, lines, style=dict()):
    spans = []
    cur = []
    for line in lines:
      if line is '':
        spans.append(Span(' '.join(cur), style))
        cur = []
      else:
        cur.append(line)

    if cur:
      spans.append(Span(' '.join(cur)))
    return spans


class FixedSpanner(Spanner):
  def span(self, lines, style=dict()):
    return [Span('\n'.join(lines), style)]



Spanner.Default = FixedSpanner()
Spanner.Prose = ProseSpanner()
Spanner.Fixed = FixedSpanner()