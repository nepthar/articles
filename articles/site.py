"""
The site model: a folder of articles that builds into a static site.

  mysite/
    site.conf        site title, author and base URL (key: value)
    articles/        blog posts in year folders: articles/2026/my-post.article
    pages/           standalone pages: pages/about.article
    static/          files copied as they are
    build/           output, ignored by git

Every post starts as a draft. A draft has a `drafted:` date and an empty
`published:` date. `articles publish` sets `published:` and moves the file
to the folder of the year it was published.
"""
import datetime
import os
import re
import shutil

from .misc import KeyValue


ConfigFile = 'site.conf'
PostsDir = 'articles'
PagesDir = 'pages'
StaticDir = 'static'
BuildDir = 'build'
Extension = '.article'


class SiteError(Exception):
  pass


def slugify(title):
  """ Make a file name from a title: "My First Post!" -> "my-first-post" """
  slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
  if not slug:
    raise SiteError(f'Cannot make a file name from the title "{title}"')
  return slug


def parse_date(value, key='date', path=None):
  """ Parse a YYYY-MM-DD date. Raise SiteError for anything else. """
  try:
    return datetime.date.fromisoformat(value)
  except ValueError:
    where = f'{path}: ' if path else ''
    raise SiteError(f'{where}{key}: "{value}" is not a YYYY-MM-DD date') from None


def split_metadata(text):
  """ Split article text into (metadata dict, body text). The metadata is
      the block of key: value lines at the top of the file.
  """
  lines = text.split('\n')
  metadata = {}
  i = 0
  while i < len(lines):
    key, value = KeyValue.extract(lines[i].rstrip())
    if key is None:
      break
    metadata[key] = value
    i += 1
  return metadata, '\n'.join(lines[i:])


def join_metadata(metadata, body):
  """ The reverse of split_metadata """
  header = '\n'.join(f'{k}: {v}'.rstrip() for k, v in metadata.items())
  return header + '\n' + body


def read_config(path):
  with open(path) as f:
    config, _ = split_metadata(f.read())
  return config


class Post:
  """ One article file in the posts folder """

  def __init__(self, site, path):
    self.site = site
    self.path = path
    with open(path) as f:
      self.metadata, self.body = split_metadata(f.read())

  @property
  def slug(self):
    return os.path.splitext(os.path.basename(self.path))[0]

  @property
  def title(self):
    return self.metadata.get('article', '')

  @property
  def author(self):
    return self.metadata.get('author') or self.site.config.get('author', '')

  @property
  def folder_year(self):
    return os.path.basename(os.path.dirname(self.path))

  @property
  def drafted(self):
    value = self.metadata.get('drafted', '')
    return parse_date(value, 'drafted', self.path) if value else None

  @property
  def published(self):
    value = self.metadata.get('published', '')
    return parse_date(value, 'published', self.path) if value else None

  @property
  def is_draft(self):
    return self.published is None

  def check(self):
    """ Return a list of problems with this post. Empty means it is fine. """
    problems = []
    if not self.title:
      problems.append(f'{self.path}: missing "article:" (the title)')
    for key in ('drafted', 'published'):
      try:
        getattr(self, key)
      except SiteError as e:
        problems.append(str(e))
    try:
      published = self.published
    except SiteError:
      published = None
    if published and self.folder_year != str(published.year):
      problems.append(
        f'{self.path}: published in {published.year} but is in the '
        f'{self.folder_year} folder. Move it to {PostsDir}/{published.year}/'
      )
    return problems

  def save(self):
    with open(self.path, 'w') as f:
      f.write(join_metadata(self.metadata, self.body))


class Site:
  def __init__(self, root):
    self.root = os.path.abspath(root)
    self.config = read_config(os.path.join(self.root, ConfigFile))

  @staticmethod
  def find(start='.'):
    """ Find the site that contains the start folder, like git does """
    path = os.path.abspath(start)
    while True:
      if os.path.isfile(os.path.join(path, ConfigFile)):
        return Site(path)
      parent = os.path.dirname(path)
      if parent == path:
        raise SiteError(f'No {ConfigFile} found here or in any parent folder. Use "articles init" to make a site.')
      path = parent

  def path(self, *parts):
    return os.path.join(self.root, *parts)

  def post_paths(self):
    """ All post files, sorted by path """
    found = []
    for folder, _, files in os.walk(self.path(PostsDir)):
      found.extend(os.path.join(folder, f) for f in files if f.endswith(Extension))
    return sorted(found)

  def posts(self):
    return [Post(self, p) for p in self.post_paths()]

  def check(self):
    """ Return a list of problems with the site. Empty means it is fine. """
    problems = []
    for post in self.posts():
      problems.extend(post.check())
    return problems

  def new_post(self, title, today=None):
    today = today or datetime.date.today()
    path = self.path(PostsDir, str(today.year), slugify(title) + Extension)
    metadata = {
      'article': title,
      'author': self.config.get('author', ''),
      'drafted': today.isoformat(),
      'published': '',
    }
    return self._create(path, metadata, PostStub)

  def new_page(self, title):
    path = self.path(PagesDir, slugify(title) + Extension)
    return self._create(path, {'article': title}, PageStub)

  def _create(self, path, metadata, body):
    if os.path.exists(path):
      raise SiteError(f'{os.path.relpath(path)} already exists')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'x') as f:
      f.write(join_metadata(metadata, body))
    return path

  def publish(self, path, today=None):
    """ Set the published date of a draft and move it to the folder of the
        year it was published. Return the new path.
    """
    today = today or datetime.date.today()
    path = os.path.abspath(path)
    if os.path.dirname(os.path.dirname(path)) != self.path(PostsDir):
      raise SiteError(f'{path} is not a post. Posts are in {PostsDir}/<year>/')

    post = Post(self, path)
    if not post.is_draft:
      raise SiteError(f'{os.path.relpath(path)} was already published on {post.published}')

    post.metadata['published'] = today.isoformat()
    post.save()

    new_path = self.path(PostsDir, str(today.year), os.path.basename(path))
    if new_path != path:
      if os.path.exists(new_path):
        raise SiteError(f'Cannot move to {os.path.relpath(new_path)}: it already exists')
      os.makedirs(os.path.dirname(new_path), exist_ok=True)
      shutil.move(path, new_path)
    return new_path


PostStub = '''

  Write the preamble here. It is the summary on the homepage.

First Section

  Write the article here.
'''

PageStub = '''

  Write the page here.
'''

WelcomeBody = '''

  This is the first post on this site. Its first paragraph, before any
  title, is the preamble. The homepage shows it as the summary.

Writing Posts

  Make a new draft with:

    articles new "My Next Post"

  Drafts have an empty "published:" date. When a draft is ready, run:

    articles publish articles/{year}/my-next-post.article
'''


def init_site(root, title=None, author='', today=None):
  """ Make a new site folder with a sample post and an about page """
  today = today or datetime.date.today()
  root = os.path.abspath(root)
  if os.path.exists(root) and os.listdir(root):
    raise SiteError(f'{root} already exists and is not empty')

  title = title or os.path.basename(root)
  os.makedirs(root, exist_ok=True)
  with open(os.path.join(root, ConfigFile), 'w') as f:
    f.write(join_metadata({'title': title, 'author': author, 'url': 'https://example.com'}, ''))
  with open(os.path.join(root, '.gitignore'), 'w') as f:
    f.write(BuildDir + '/\n')
  os.makedirs(os.path.join(root, StaticDir))

  site = Site(root)
  site.new_page('About')
  welcome = site.path(PostsDir, str(today.year), 'welcome' + Extension)
  site._create(welcome, {
    'article': 'Welcome',
    'author': author,
    'drafted': today.isoformat(),
    'published': today.isoformat(),
  }, WelcomeBody.format(year=today.year))
  return site
