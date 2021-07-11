#from spans import Spanner
from elements import *

class BlockDecoder:
  # The block identifier prefix ("quote: ")
  kind = None

  def decodeBlock(self, blockLines, argString):
    raise NotImplementedError


class SimpleBlockDecoder(BlockDecoder):
  kind = None
  spanner = None
  element = None

  def decodeBlock(self, lines, argString):
    e = self.element(self.spanner.span(lines))
    e.args = argString
    return (e,)


class NoteDecoder(SimpleBlockDecoder):
  kind = 'note'
  spanner = Spanner.Prose
  element = NoteElement


class FootnoteDecoder(SimpleBlockDecoder):
  kind = 'footnote'
  spanner = Spanner.Prose
  element = FootnoteElement


class MarginNoteDecoder(SimpleBlockDecoder):
  kind = 'margin'
  spanner = Spanner.Prose
  element = MarginNoteElement


class InlineNoteDecoder(SimpleBlockDecoder):
  kind = 'inline'
  spanner = Spanner.Prose
  element = InlineNoteElement


class FixedTextDecoder(SimpleBlockDecoder):
  kind = 'fixed'
  spanner = Spanner.Fixed
  element = FixedWidthBlockElement


class QuoteDecoder(SimpleBlockDecoder):
  # TODO: Have this handle quote attribution instead of just being a
  # simple decoder.
  kind = 'quote'
  spanner = Spanner.Fixed
  element = BlockQuoteElement


class CodeDecoder(BlockDecoder):
  kind = 'code'
  spanner = Spanner.Fixed

  def decodeBlock(self, lines, argString):
    e = CodeBlockElement(self.spanner.span(lines))
    e.lang = argString
    return (e,)
