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
    return self.next.finish()


class FrameDumper(PipelineElement):
  def __init__(self):
    self.frames = []

  def handle(self, frame):
    self.frames.append(frame)


  def finish(self):
    for i, f in enumerate(self.frames):

      print(f"{i}: {f}")
      if f.lines:
        print('\n'.join(f"  |{l}" for l in f.lines))

      print('')
    return self.next.finish()


class Accumulator(PipelineElement):
  def __init__(self):
    self.accum = []

  def handle(self, element):
    self.accum.append(element)


class HTMLFrameDumper(PipelineElement):
  def __init__(self):
    self.i = 0

  def handle(self, frame):
    if self.i == 0:
      self.next.handle("<html><body>")

    self.i += 1
    self.next.handle(f"<h2>Frame {self.i}, Prefix:|{frame.prefix}|</h2>")
    fmt = '\n'.join(frame.lines)
    self.next.handle(f"<pre>{fmt}</pre>")

  def finish(self):
    self.next.handle("</body></html>")
    return self.next.finish()