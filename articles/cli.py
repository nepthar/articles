import argparse
import logging
import os
import sys

from .pipeline import Pipeline, SimpleHandler
from .framing import LineFramer
from .decoders import (
  FrameDecoder, EmptyDecoder, InvalidDecoder, MetadataDecoder, CommentDecoder,
  TitleDecoder, ParagraphDecoder, BlockDecoder,
)
from .list_decoder import ListDecoder
from .blocks import BlockDirectiveHandler
from .elements import IdentifyElements
from .articles import ArticleBuilder
from .render import SimpleHTMLRenderer
from .text import InlineMarkdownStyleizer


logger = logging.getLogger(__name__)


class RightStripCharacters(SimpleHandler):
  function = lambda x: x.rstrip('\r\n\t ')


def create_pipeline():
  """ Create the pipeline that turns lines of an article into HTML lines """
  decoders = [
    EmptyDecoder(),
    InvalidDecoder(),
    MetadataDecoder(),
    CommentDecoder(),
    TitleDecoder(),
    ParagraphDecoder(),
    BlockDecoder(),
    ListDecoder(),
  ]
  return Pipeline([
    RightStripCharacters(),
    LineFramer(),
    FrameDecoder(decoders=decoders),
    BlockDirectiveHandler(),
    IdentifyElements(),
    ArticleBuilder(stylizer=InlineMarkdownStyleizer()),
    SimpleHTMLRenderer(),
  ])


def render_text(lines):
  """ Render an iterable of article lines to one HTML string """
  return '\n'.join(str(x) for x in create_pipeline().process(lines)) + '\n'


def render(args):
  if not os.path.exists(args.input_file):
    logger.error(f"Input file not found: {args.input_file}")
    return 1

  with open(args.input_file) as f:
    output = render_text(f)

  if args.output == '-':
    sys.stdout.write(output)
    return 0

  # The default output file has the same name with an .html extension
  out_path = args.output or os.path.splitext(args.input_file)[0] + '.html'
  with open(out_path, 'w') as f:
    f.write(output)
  logger.info(f"Output written to {out_path}")
  return 0


def main(argv=None):
  parser = argparse.ArgumentParser(prog='articles', description='Articles text format tools')
  parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging')
  commands = parser.add_subparsers(dest='command', required=True)

  render_cmd = commands.add_parser('render', help='Render one article file to HTML')
  render_cmd.add_argument('input_file', help='Input article file')
  render_cmd.add_argument('-o', '--output', help="Output HTML file, or '-' for stdout")
  render_cmd.set_defaults(func=render)

  args = parser.parse_args(argv)
  logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
  return args.func(args)
