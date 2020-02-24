# 1. All of the lines of the file are in an array  array
# 2. Comment lines are removed
# 3. Split into chunks on two consecutive newlines
# 4. Parsed that way.

import sys
from nouns import *
from pipeline import *


a = Accumulator()

elements = [
  StripRightWhitespace(),
  NewlineFramer(),
  IndentFramer(),
  CommentFramer(),
  FrameDecoder(),
  Logger(),
  a
]
pipeline = Pipeline(elements)
pipeline.process(sys.stdin)

for x in a.result():
  print(x)
