from collections import namedtuple
import re

from text import collect_poetry, collect_prose
from elements import *
from framing import ListFrame
from pipeline import Handler
from decoders import Decoder


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

  @staticmethod
  def to_regex(part):
    return re.compile(r"^" + part + r"\s+")

  def __init__(self, patterns=None):
    self.patterns = patterns if patterns is not None else self.ItemPatterns
    self._reset()

  def _reset(self):
    self.current_item = []
    self.items = []
    self.ordered = False
    self.type = None

  def _finish_item(self):
    if self.current_item:
      self.items.append(collect_prose(self.current_item))
    self.current_item = []

  def _find_item_pattern(self, first_line):
    for ipattern in self.patterns:
      if ipattern.regex.match(first_line):
        return ipattern
    return None

  def _discover_prefix(self, first_line):
    """
    Discover the list item prefix pattern from the first line.
    Returns a tuple of (pattern, regex) or None if no pattern matches.
    """
    pattern = self._find_item_pattern(first_line)
    if pattern:
      self.ordered = pattern.order_type is not None
      self.type = pattern.order_type
      return (pattern, pattern.regex)
    return None

  def decode(self, frame):
    if len(frame.lines) == 0:
      return [InvalidElement("Empty list frame")]

    self._reset()
    prefix = self._discover_prefix(frame.lines[0])

    if prefix is None:
      return [InvalidElement(collect_poetry(frame.lines))]

    pr = prefix[1]

    for line in frame.lines:

      if len(line) == 0:
        self._finish_item()

      else:
        m = re.match(pr, line)

        if m:
          # This means we've matched the item prefix
          self._finish_item()

          # Strip the prefix off and append it to the current item
          cut_line = line[m.span()[1]:]
          self.current_item.append(cut_line)

        else:
          # Otherwise strip whitespace and append. I think this works
          # okay, but I doubt I've covered every edge case.
          self.current_item.append(line.strip())

    # Finish any existing item
    self._finish_item()

    return [ListElement(self.items, order_type=self.type)]













