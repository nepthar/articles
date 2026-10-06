import re

from .text import Span, collect_poetry, collect_prose
from .elements import *
from .framing import ListFrame
from .pipeline import Handler
from .decoders import Decoder


class ItemPattern:
  def __init__(self, name, regex, order_type):
    self.name = name
    self.regex = re.compile(r"^" + regex + r"\s+")
    self.order_type = order_type


class ListDecoder(Decoder):
  """
  Converts a list frame to either an ordered or unordered list. Future
  work could also include this handling "dictionary" type structures,
  where you have a list of term: definition pairs.
  """
  FrameClass = ListFrame

  # Sorted list of prefixes to look for which indicate a new list item
  ItemPatterns = [
    ## TODO: Add roman numerals here
    ItemPattern('lc',   r"[a-z]{1,2}\.",  'a'),
    ItemPattern('uc',   r"[A-Z]{1,2}\.",  'A'),
    ItemPattern('plus', r"\+",            '1'),
    ItemPattern('num',  r"[0-9]{1,3}\.",  '1'),
    ItemPattern('dash', r"\-",            None),
    ItemPattern('star', r"\*",            None),
    ItemPattern('o',    r"o",             None),
  ]

  def __init__(self, patterns=None):
    self.patterns = patterns if patterns is not None else self.ItemPatterns

  def _find_item_pattern(self, line):
    """ Return the pattern that starts a list item on this line, or None.
        Only a line with no leading whitespace can start an item. Indented
        lines continue the current item, so wrapped text never starts a
        new item by accident.
    """
    if not line or line[0].isspace():
      return None
    for ipattern in self.patterns:
      if ipattern.regex.match(line):
        return ipattern
    return None

  @staticmethod
  def _start(pattern, line):
    """ The number of the first item, for lists that do not start at 1 """
    marker = line.split(None, 1)[0].rstrip('.')
    if pattern.name == 'num':
      return int(marker)
    if pattern.name in ('lc', 'uc') and len(marker) == 1:
      return ord(marker.lower()) - ord('a') + 1
    return 1

  def decode(self, frame):
    if len(frame.lines) == 0:
      return [InvalidElement([Span("Empty list frame")])]

    if self._find_item_pattern(frame.lines[0]) is None:
      return [InvalidElement(collect_poetry(frame.lines))]

    lists = []      # finished ListElements
    items = []      # items of the current list
    current = []    # lines of the current item
    pattern = None  # item pattern of the current list
    start = 1

    def finish_item():
      if current:
        items.append(collect_prose(current))
      current.clear()

    def finish_list():
      finish_item()
      if items:
        lists.append(ListElement(list(items), order_type=pattern.order_type, start=start))
      items.clear()

    for line in frame.lines:
      if not line:
        finish_item()
        continue

      found = self._find_item_pattern(line)
      if found is None:
        # A continuation of the current item
        current.append(line.strip())
        continue

      if found is not pattern:
        # A different prefix starts a new list
        finish_list()
        pattern = found
        start = self._start(found, line)

      finish_item()
      current.append(line[found.regex.match(line).end():])

    finish_list()
    return lists
