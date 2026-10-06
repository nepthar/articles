"""
Tests for the render path. Run with: python3 -m unittest discover -s test
"""
import glob
import os
import subprocess
import sys
import unittest

from articles.cli import render_text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = sorted(glob.glob(os.path.join(ROOT, 'samples', '**', '*.article'), recursive=True))


def render(text):
  return render_text(text.splitlines())


class TestSamples(unittest.TestCase):
  def test_samples_exist(self):
    self.assertTrue(SAMPLES)

  def test_every_sample_renders(self):
    for path in SAMPLES:
      with self.subTest(sample=os.path.relpath(path, ROOT)):
        with open(path) as f:
          html = render_text(f)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('</html>', html)


class TestElements(unittest.TestCase):
  def test_metadata_sets_title(self):
    html = render("article: Hello\nauthor: Me\n\n\nIntro\n\n  Some text.\n")
    self.assertIn('<title>Hello</title>', html)
    self.assertIn('<p>Some text.</p>', html)

  def test_paragraph_lines_join(self):
    html = render("Title\n\n  one\n  two\n")
    self.assertIn('<p>one two</p>', html)

  def test_comments_are_not_published(self):
    html = render("Title\n\n  // secret note\n  Visible.\n")
    self.assertNotIn('secret', html)
    self.assertIn('Visible.', html)

  def test_plain_block_keeps_line_breaks(self):
    html = render("Title\n\n    line one\n    line two\n")
    self.assertIn('<pre>line one\nline two</pre>', html)

  def test_code_block(self):
    html = render("Title\n\n    code: python, 3.8\n    x = 1\n")
    self.assertIn('<pre><code>x = 1</code></pre>', html)

  def test_unordered_list(self):
    html = render("Title\n\n   - eggs\n   - milk\n")
    self.assertIn('<ul>\n<li>eggs</li>\n<li>milk</li>\n</ul>', html)

  def test_ordered_list(self):
    html = render("Title\n\n   1. eggs\n   2. milk\n")
    self.assertIn('<ol>', html)


class TestCommand(unittest.TestCase):
  def run_articles(self, *args):
    return subprocess.run(
      [sys.executable, '-m', 'articles', *args],
      cwd=ROOT, capture_output=True, text=True,
    )

  def test_render_to_stdout(self):
    result = self.run_articles('render', 'samples/simple.article', '-o', '-')
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn('<!DOCTYPE html>', result.stdout)

  def test_render_to_file(self):
    out = os.path.join(ROOT, 'test', '_out.html')
    try:
      result = self.run_articles('render', 'samples/simple.article', '-o', out)
      self.assertEqual(result.returncode, 0, result.stderr)
      with open(out) as f:
        self.assertIn('<!DOCTYPE html>', f.read())
    finally:
      if os.path.exists(out):
        os.remove(out)

  def test_missing_file(self):
    result = self.run_articles('render', 'nope.article')
    self.assertEqual(result.returncode, 1)

  def test_render_uses_only_the_standard_library(self):
    # The simple path must never need a third-party package (e.g. jinja2).
    code = (
      "import sys\n"
      "before = set(sys.modules)\n"
      "from articles.cli import render_text\n"
      "render_text(open('samples/basic.article'))\n"
      "loaded = {m.split('.')[0] for m in set(sys.modules) - before}\n"
      "print(','.join(sorted(loaded - set(sys.stdlib_module_names) - {'articles'})))\n"
    )
    result = subprocess.run([sys.executable, '-c', code], cwd=ROOT, capture_output=True, text=True)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), '')


if __name__ == '__main__':
  unittest.main()
