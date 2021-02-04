#!/usr/bin/env python3
import sys

from src.framing import *
from src.pipeline import *


class RightStripCharacters(SimpleHandler):
  function = lambda x: x.rstrip('\r\n\t ')

handlers = [
  RightStripCharacters(),
  LineFramer()
]

result = Pipeline(handlers).process(sys.stdin)

print(result)

