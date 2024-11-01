from enum import Enum

from text import collect_poetry, collect_prose
from elements import *
from framing import ListFrame
from pipeline import Handler

from decoders import Decoder


import re

class ListDecoder(Decoder):
  """
  Converts a list frame to either an ordered or unordered list. Future
  work could also include this handling "dictionary" type structures,
  where you have a list of term: definition pairs.
  """
  FrameClass = ListFrame

  # These start a new ordered list item
  OrderedPatterns = [
    ('alnum', r"[a-zA-Z0-9]\."),
    ('plus',  r"\+")
  ]

  # These start a new unordered list item
  UnorderedPatterns = [
    ('dash', r"\-"),
    ('star', r"\*"),
    ('o',    r"o")
  ]

  @staticmethod
  def to_regex(part):
    return re.compile(r"^" + part + r"\s+")

  def __init__(self):
    # TODO: This seems messy, consider reworking
    self.o_patterns = {
      name: ListDecoder.to_regex(p) for name, p in self.OrderedPatterns
    }

    self.u_patterns = {
      name: ListDecoder.to_regex(p) for name, p in self.UnorderedPatterns
    }

  def _reset(self):
    self.current_item = []
    self.items = []
    self.ordered = False
    self.prefix = None

  def _finish_item(self):
    if self.current_item:
      self.items.append(collect_prose(self.current_item))
    self.current_item = []

  def _set_prefix(self, first_line):
    for name, ptrn in self.u_patterns.items():
      if re.match(ptrn, first_line):
        self.prefix = (name, ptrn)
        return

    for name, ptrn in self.o_patterns.items():
      if re.match(ptrn, first_line):
        self.ordered = True
        self.prefix = (name, ptrn)
        return

  def decode(self, frame):
    if len(frame.lines) == 0:
      return [InvalidElement("Empty list frame")]

    self._reset()
    self._set_prefix(frame.lines[0])

    if self.prefix is None:
      return [InvalidElement(collect_poetry.collect(frame.lines))]

    pr = self.prefix[1]

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

    return [ListElement(self.items, ordered=self.ordered)]













