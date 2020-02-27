# 1. All of the lines of the file are in an array  array
# 2. Comment lines are removed
# 3. Split into chunks on two consecutive newlines
# 4. Parsed that way.

import sys
import gc
from nouns import *
from pipeline import *

gc.disable()


a = Accumulator()

elements = [
  StripRight(),
  NewlineFramer(),
  IndentFramer(),
  CommentFramer(),
  RawFrameTyper(),
  Logger(),
  a
]
pipeline = Pipeline(elements)
pipeline.process(sys.stdin)

for x in a.result():
  print(x)
