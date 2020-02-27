# 1. All of the lines of the file are in an array  array
# 2. Comment lines are removed
# 3. Split into chunks on two consecutive newlines
# 4. Parsed that way.

import sys
import gc
from pipeline import *

gc.disable()

m = MetadataReader()

elements = [
  EmptyLineSegmenter(),
  IndentSegmenter(),
  m,
  SegmentSanity(),
  TextReflowHandler(),
  LinePrinter()
]

Pipeline(elements).process(sys.stdin)
print(m.metadata)
