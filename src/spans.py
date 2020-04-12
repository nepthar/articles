# Styles: emphasis, strong, strikethrough, underline

class Span:
  def __init__(self, text, **style):
    self.text = text
    self.style = style


  # def clearStyle(self):
  #   self.st.clear()

  # def getStyle(self, key, default=None):
  #   if key in self.st:
  #     return self.st[key]
  #   elif self.parent:
  #     return self.parent.getStyle(key, default)
  #   else:
  #     return default

  # def setStyle(self, key, value=''):
  #   self.st[key] = value


Span.Empty = Span('')


class Spanner:
  pass


class ProseSpanner(Spanner):
  def span(self, lines):
    spans = []
    cur = []
    for line in lines:
      if line is '':
        spans.append(Span(' '.join(cur)))
        cur = []
      else:
        cur.append(line)

    if cur:
      spans.append(Span(' '.join(cur)))
    return spans


class FixedSpanner(Spanner):
  def span(self, lines):
    return [Span('\n'.join(lines))]


Spanner.Default = FixedSpanner()
Spanner.Prose = ProseSpanner()
Spanner.Fixed = FixedSpanner()