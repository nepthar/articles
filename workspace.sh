# workspace.sh // Common Vars & Operations

workspace="articles"

# This file is designed to work with shell tools, but it can be used
# without them by sourcing this directly. If used with shell tools, the
# commands prefixed with 'articles' will be run from the same dir as
# this file in a subshell.

source ./src/.venv/bin/activate

articles.test-basic() {
  python3 ./src < ./samples/basic.article
}

articles.unused-code()
{
  python3 -m vulture src/__main__.py
}
