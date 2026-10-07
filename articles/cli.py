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
from . import site as sitemod


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


def init(args):
  site = sitemod.init_site(args.folder, title=args.title, author=args.author or '')
  print(f'Made a new site in {os.path.relpath(site.root)}')
  return 0


def new(args):
  site = sitemod.Site.find()
  if args.page:
    path = site.new_page(args.title)
  else:
    path = site.new_post(args.title)
  print(os.path.relpath(path))
  return 0


def publish(args):
  site = sitemod.Site.find(os.path.dirname(os.path.abspath(args.file)))
  path = site.publish(args.file)
  print(os.path.relpath(path))
  return 0


def check(args):
  site = sitemod.Site.find()
  problems = site.check()
  for p in problems:
    print(p)
  return 1 if problems else 0


def main(argv=None):
  parser = argparse.ArgumentParser(prog='articles', description='Articles text format tools')
  parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging')
  commands = parser.add_subparsers(dest='command', required=True)

  render_cmd = commands.add_parser('render', help='Render one article file to HTML')
  render_cmd.add_argument('input_file', help='Input article file')
  render_cmd.add_argument('-o', '--output', help="Output HTML file, or '-' for stdout")
  render_cmd.set_defaults(func=render)

  init_cmd = commands.add_parser('init', help='Make a new site folder')
  init_cmd.add_argument('folder', help='Folder for the new site')
  init_cmd.add_argument('--title', help='Site title (default: the folder name)')
  init_cmd.add_argument('--author', help='Default author for new posts')
  init_cmd.set_defaults(func=init)

  new_cmd = commands.add_parser('new', help='Make a new draft post, or a page with --page')
  new_cmd.add_argument('title', help='Title of the post or page')
  new_cmd.add_argument('--page', action='store_true', help='Make a page instead of a post')
  new_cmd.set_defaults(func=new)

  publish_cmd = commands.add_parser('publish', help='Publish a draft post with today\'s date')
  publish_cmd.add_argument('file', help='The draft post file')
  publish_cmd.set_defaults(func=publish)

  check_cmd = commands.add_parser('check', help='Check every post for metadata problems')
  check_cmd.set_defaults(func=check)

  args = parser.parse_args(argv)
  logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
  try:
    return args.func(args)
  except sitemod.SiteError as e:
    print(f'articles: {e}', file=sys.stderr)
    return 1
