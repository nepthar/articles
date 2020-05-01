from decoders import *
from blocks import BlockDecoder


class Default:
  @staticmethod
  def decoderConfig():
    return DecoderConfig(
      MetadataDecoder(),
      TitleDecoder(),
      BreakDecoder(),
      CommentDecoder(),
      ParagraphDecoder(),
      BlockDecodeDispatcher(
        default='quote',
        decoders=[
          BlockDecoder('footnote', FootnoteElement, Spanner.Prose),
          BlockDecoder('margin', MarginNoteElement, Spanner.Prose),
          BlockDecoder('inline', InlineNoteElement, Spanner.Prose),
          BlockDecoder('fixed', FixedWidthBlockElement, Spanner.Fixed),
          BlockDecoder('code', CodeBlockElement, Spanner.Fixed),
          BlockDecoder('quote', BlockQuoteElement, Spanner.Fixed),
        ]),
    )
