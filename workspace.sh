# workspace.sh // Common Vars & Operations

workspace="articles"

# This file is designed to work with shell tools, but it can be used
# without them by sourcing this directly. If used with shell tools, the
# commands prefixed with 'articles' will be run from the same dir as
# this file in a subshell.

articles.todo() {
cat << TODO

  - Finish the HTML renderer. How will it work? Maybe renderers should all just be
    (Article) -> [text]? Or new Renderer(article), renderer.configure(...),
    renderer.write(fileobject).
    Think about how to best plug it in with a templating system that will
    ultimately be used for static site creation. Maybe start with writing
    travel-blog and then write articles HTML generation once you know how
    it's going to be used.

  - Make a terminal renderer with rich.py https://github.com/willmcgugan/rich

  - Make a .article renderer which will essentially be a formatter.

  - Finish Serde package so you can have language interp

  - Links & Spans: Finish defining:
    - ''Multi word link''<1>
    - Single word <slug> link
    - Multi ''word slug link''<multi>
    - Link to a footnote<f1>.
    - Bleh

  - Lists, ordered lists (v1)

  - Section auto-numbering, TOC generation

  - What else?

TODO
}

articles.test-basic() {
  python3 ./src < ./samples/basic.article
}

articles.unused-code()
{
  python3 -m vulture src/articles.py
}
