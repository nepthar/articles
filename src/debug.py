from pipeline import PipelineElement

class AnyPrinter(PipelineElement):
  def __init__(self):
    self.i = 0

  def handle(self, item):
    print(f"{item}")

  def finish(self):
    print("<flush>")


class LinePrinter(PipelineElement):
  def handle(self, line):
    print(line)

  def finish(self):
    pass

class ElementDumper(PipelineElement):
  def __init__(self):
    self.i = 0

  def spanString(self, span):
    unNewlined = span.text.replace('\n', '\\n')
    return f'  | {unNewlined}'


  def handle(self, elem):
    l = [f'--[ {self.i}: {elem.__class__.__name__} :: {elem.kind} ]--']
    l.extend(self.spanString(s) for s in elem.spans)
    l.append(f'--[ {self.i}: end ]--')
    l.append('\n')
    print('\n'.join(l))
    self.i += 1


  def finish(self):
    print("-- finish --")


class FrameDumper(PipelineElement):
  def __init__(self):
    self.i = 0

  def handle(self, frame):
    self.i += 1
    lines = '\n'.join(f" |{l}" for l in frame.lines)
    print(f"Frame {self.i}. Prefix: |{frame.prefix}|\n{lines}\n")
    self.next.handle(frame)

  def finish(self):
    print("<flush>")
    self.next.finish()


class Accumulator(PipelineElement):
  def __init__(self):
    self.accum = []

  def handle(self, element):
    self.accum.append(element)

  def finish(self):
    pass




class TermColors:
  clear = '\033[0m'

  fg = {
    'reset': '\033[0m',
    'bold': '\033[01m',
    'underline': '\033[04m',
    'strike': '\033[08m',

    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'orange': '\033[33m',
    'blue': '\033[34m',
    'purple': '\033[35m',
    'cyan': '\033[36m',
    'lightgrey': '\033[37m',
    'darkgrey': '\033[90m',
    'lightred': '\033[91m',
    'lightgreen': '\033[92m',
    'yellow': '\033[93m',
    'lightblue': '\033[94m',
    'pink': '\033[95m',
    'lightcyan': '\033[96m',
  }



class TerminalRenderer(PipelineElement):

  fixed = set(('code', 'fixed'))

  styleMap = {
    'h0': ('bold', 'underline'),
    'h1': ('bold', 'underline'),
    'h2': ('underline'),
    'quote': ('lightgrey'),
    'code': ('green',),
  }

  def __init__(self, width=76):
    self.tw = textwrap.TextWrapper(width=width)

  def printSpan(self, span):

    print(self.tw.fill(span.text))

  def printFixed(self, cls, span):
    print(span.text)


  def getNumberedLines(self, prefix, span):
    i = 0
    numbered = []
    for line in span.text.splitlines():
      numbered.append(f'{prefix}{i}: {line}')
    return '\n'.join(numbered)

  def styleString(self, rc, span):
    if rc in self.styleMap:
      styles = [TermColors.fg[x] for x in self.styleMap[rc]]
      ss = ''.join(styles)
      return f'{ss}{span.text}{TermColors.clear}'
    else:
      return span.text

  def handle(self, elem):
    rc = elem.renderClass

    styledJoined = ''.join(self.styleString(rc, s) for s in elem.spans)

    print(styledJoined)
    print('')

  def finish(self):
    pass
