"""
Tests for the site model and the init, new, publish and check commands.
"""
import datetime
import os
import subprocess
import sys
import tempfile
import unittest

from articles import site as s

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = datetime.date


class TestHelpers(unittest.TestCase):
  def test_slugify(self):
    self.assertEqual(s.slugify('My First Post!'), 'my-first-post')
    self.assertEqual(s.slugify('  C++ & Rust  '), 'c-rust')

  def test_slugify_rejects_empty(self):
    with self.assertRaises(s.SiteError):
      s.slugify('!!!')

  def test_parse_date(self):
    self.assertEqual(s.parse_date('2026-10-05'), D(2026, 10, 5))

  def test_parse_date_rejects_free_text(self):
    with self.assertRaises(s.SiteError):
      s.parse_date('March 2021')

  def test_metadata_round_trip(self):
    text = 'article: Hi\npublished:\n\n\n  Body.\n'
    md, body = s.split_metadata(text)
    self.assertEqual(md, {'article': 'Hi', 'published': ''})
    self.assertEqual(s.join_metadata(md, body), text)


class SiteTest(unittest.TestCase):
  def setUp(self):
    self.tmp = tempfile.TemporaryDirectory()
    self.root = os.path.join(self.tmp.name, 'blog')
    self.site = s.init_site(self.root, title='Blog', author='Jordan', today=D(2026, 10, 5))

  def tearDown(self):
    self.tmp.cleanup()

  def read(self, path):
    with open(path) as f:
      return f.read()


class TestInit(SiteTest):
  def test_layout(self):
    for path in ['site.conf', '.gitignore', 'static', 'pages/about.article', 'articles/2026/welcome.article']:
      self.assertTrue(os.path.exists(os.path.join(self.root, path)), path)

  def test_config(self):
    self.assertEqual(self.site.config['title'], 'Blog')
    self.assertEqual(self.site.config['author'], 'Jordan')

  def test_welcome_is_published(self):
    [post] = self.site.posts()
    self.assertEqual(post.published, D(2026, 10, 5))
    self.assertEqual(self.site.check(), [])

  def test_refuses_non_empty_folder(self):
    with self.assertRaises(s.SiteError):
      s.init_site(self.root)


class TestNew(SiteTest):
  def test_new_post_is_a_draft(self):
    path = self.site.new_post('Hello World', today=D(2026, 12, 1))
    self.assertEqual(path, os.path.join(self.root, 'articles', '2026', 'hello-world.article'))
    post = s.Post(self.site, path)
    self.assertEqual(post.title, 'Hello World')
    self.assertEqual(post.author, 'Jordan')
    self.assertEqual(post.drafted, D(2026, 12, 1))
    self.assertTrue(post.is_draft)

  def test_new_post_goes_in_current_year(self):
    path = self.site.new_post('Later', today=D(2027, 1, 2))
    self.assertIn(os.path.join('articles', '2027'), path)

  def test_new_post_refuses_existing(self):
    self.site.new_post('Twice')
    with self.assertRaises(s.SiteError):
      self.site.new_post('Twice')

  def test_new_page(self):
    path = self.site.new_page('Now')
    self.assertEqual(path, os.path.join(self.root, 'pages', 'now.article'))
    self.assertTrue(self.read(path).startswith('article: Now\n'))


class TestPublish(SiteTest):
  def test_publish_same_year(self):
    path = self.site.new_post('Post', today=D(2026, 11, 1))
    new_path = self.site.publish(path, today=D(2026, 11, 2))
    self.assertEqual(new_path, path)
    self.assertEqual(s.Post(self.site, path).published, D(2026, 11, 2))

  def test_publish_moves_to_new_year(self):
    path = self.site.new_post('Post', today=D(2026, 12, 30))
    new_path = self.site.publish(path, today=D(2027, 1, 2))
    self.assertEqual(new_path, os.path.join(self.root, 'articles', '2027', 'post.article'))
    self.assertFalse(os.path.exists(path))
    post = s.Post(self.site, new_path)
    self.assertEqual(post.drafted, D(2026, 12, 30))
    self.assertEqual(post.published, D(2027, 1, 2))
    self.assertEqual(self.site.check(), [])

  def test_publish_keeps_body(self):
    path = self.site.new_post('Post')
    before = s.Post(self.site, path).body
    self.site.publish(path)
    self.assertEqual(s.Post(self.site, path).body, before)

  def test_publish_twice_fails(self):
    path = self.site.new_post('Post')
    self.site.publish(path)
    with self.assertRaises(s.SiteError):
      self.site.publish(path)

  def test_publish_page_fails(self):
    with self.assertRaises(s.SiteError):
      self.site.publish(os.path.join(self.root, 'pages', 'about.article'))


class TestCheck(SiteTest):
  def write_post(self, year, name, text):
    path = os.path.join(self.root, 'articles', year, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
      f.write(text)

  def test_missing_title(self):
    self.write_post('2026', 'x.article', 'drafted: 2026-01-01\npublished:\n')
    [problem] = self.site.check()
    self.assertIn('missing "article:"', problem)

  def test_bad_date(self):
    self.write_post('2026', 'x.article', 'article: X\ndrafted: March 2021\npublished:\n')
    [problem] = self.site.check()
    self.assertIn('drafted: "March 2021"', problem)

  def test_wrong_year_folder(self):
    self.write_post('2025', 'x.article', 'article: X\npublished: 2026-02-02\n')
    [problem] = self.site.check()
    self.assertIn('Move it to articles/2026/', problem)


class TestCommands(unittest.TestCase):
  def run_articles(self, cwd, *args):
    env = dict(os.environ, PYTHONPATH=ROOT)
    return subprocess.run(
      [sys.executable, '-m', 'articles', *args],
      cwd=cwd, env=env, capture_output=True, text=True,
    )

  def test_init_new_publish(self):
    with tempfile.TemporaryDirectory() as tmp:
      result = self.run_articles(tmp, 'init', 'blog', '--author', 'Jordan')
      self.assertEqual(result.returncode, 0, result.stderr)
      blog = os.path.join(tmp, 'blog')

      # new finds the site from a sub folder, like git
      result = self.run_articles(os.path.join(blog, 'pages'), 'new', 'Hello')
      self.assertEqual(result.returncode, 0, result.stderr)
      year = str(datetime.date.today().year)
      draft = os.path.join(blog, 'articles', year, 'hello.article')
      self.assertTrue(os.path.exists(draft))

      result = self.run_articles(blog, 'publish', draft)
      self.assertEqual(result.returncode, 0, result.stderr)

      result = self.run_articles(blog, 'check')
      self.assertEqual(result.returncode, 0, result.stdout)

  def test_new_outside_a_site(self):
    with tempfile.TemporaryDirectory() as tmp:
      result = self.run_articles(tmp, 'new', 'Hello')
      self.assertEqual(result.returncode, 1)
      self.assertIn('No site.conf found', result.stderr)


if __name__ == '__main__':
  unittest.main()
