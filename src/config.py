from __main__ import FrameSer
from decoders import *
from blocks import BlockDecoder
from framing import DefaultFramer
from pipeline import OutputWriter


class Default:
  @staticmethod
  def decoderConfig():
    return DecoderConfig(
      MetadataDecoder(),
      TitleDecoder(),
      ParagraphDecoder(),
      BlockDecodeDispatcher(
        default='quote',
        decoders=[
          BlockDecoder('footnote', FootnoteElement, Spanner.Prose),
          BlockDecoder('inline', InlineNoteElement, Spanner.Prose),
          BlockDecoder('fixed', FixedWidthBlockElement, Spanner.Fixed),
          BlockDecoder('code', CodeBlockElement, Spanner.Fixed),
          BlockDecoder('quote', BlockQuoteElement, Spanner.Fixed),
        ]),
    )

  @staticmethod
  def framingPipeline():
    return [
      DefaultFramer(),
      FrameSer(),
      OutputWriter()
    ]

  @staticmethod
  def textRenderPipeline():
    decoders = Default.decoderConfig()
    return []

