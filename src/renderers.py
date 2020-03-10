from pipeline import PipelineElement
import textwrap


class Renderer(PipelineElement):
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
