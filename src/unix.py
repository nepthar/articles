#!/usr/bin/env python3


import sys
from pipeline import *


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

