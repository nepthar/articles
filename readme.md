

Articles

  I hate markdown and really like the look/feel of RFCs. I've made Articles in
  an effort to mix the two in a more visually appealing way.


Usage

  Install the articles command with uv:

    uv tool install git+https://github.com/nepthar/articles

  Render one article to an HTML file next to it. Use "-o -" to print the
  HTML instead.

    articles render post.article
    articles render post.article -o -

  Make a site. A site is a folder with a site.conf file, posts in
  articles/<year>/, and pages in pages/.

    articles init mysite --author "Your Name"

  Inside the site folder, make a draft post or a page. Every post starts
  as a draft with an empty "published:" date.

    articles new "My First Post"
    articles new --page "Now"

  Publish a draft. This sets "published:" to today and moves the file to
  the folder of the current year if it is not there already.

    articles publish articles/2026/my-first-post.article

  Check every post for metadata problems, such as a bad date:

    articles check

  The example/ folder is a fake blog for trying changes by hand. It has
  posts over three years, a draft, pages, and every list and block form.

    cd example
    articles check

  Run the tests from the repository root:

    python3 -m unittest discover -s test


Paragraphs

  Paragraphs are indented two spaces. All single newlines are removed and
  replaced with a space.
  That means this is the same paragraph.

  However, this is a new paragraph.


Sections and Headings

  Headings



Lists

  Lists are something I'm still struggling with. I'm not sure what the format
  should look like just yet. Ideally, there should be a way to provide three
  things - ordered, unordered, and dictionaries.

Ordered lists

  An order