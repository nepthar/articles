old.py

# class EmptyLineSegmenter(PipelineElement):
#   """ Calls finish whenever there's two empty lines in a row """
#   def __init__(self, limit=2):
#     self.nlCount = 0
#     self.limit = limit

#   def handle(self, line):
#     if line is '':
#       self.nlCount += 1
#     else:
#       self.nlCount = 0

#     if self.nlCount < self.limit:
#       self.next.handle(line)

#     elif self.nlCount == self.limit:
#       self.finish()

# class LinesFramer(PipelineElement):
#   def __init__(self):
#     self.accum = []
#     self.count = 0

#   def handle(self, line):
#     self.accum.append(line)

#   def finish(self):
#     lines = self.accum
#     while lines and lines[-1] == '':
#       lines.pop()

#     if lines:
#       # Ignore empty lines when finding a common prefix
#       prefix = Text.commonWsPrefix(lines, ignoreEmpty=True)
#       if prefix:
#         li = len(prefix)
#         self.next.handle(Frame(self.count, [l[li:] for l in lines], prefix))
#       else:
#         self.next.handle(Frame(self.count, lines))

#       self.count += 1
#       self.next.finish()

#     self.accum = []

# class MetadataReader(PipelineElement):
#   def __init__(self):
#     self.metadata = {}
#     self.done = False

#   def handle(self, line):
#     if self.done:
#       self.next.handle(line)
#     else:
#       key, val = KeyValue.extract(line)
#       if key:
#         self.metadata[key] = val
#       else:
#         self.warn(f"Bad KV Pair: {line}")

#   def finish(self):
#     self.done = True
#     self.next.finish()
