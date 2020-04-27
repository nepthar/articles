# workspace.sh // Common Vars & Operations

workspace="articles"

# This file is designed to work with shell tools, but it can be used
# without them by sourcing this directly. If used with shell tools, the
# commands prefixed with '{{name}}.' will be run from the same dir as
# this file in a subshell.

articles.test-basic() {
  python3 ./src < ./samples/basic.article
}

articles.pwd() {
  echo $PWD
  echo $SHLVL
  ws.info
}

articles.todo() {
  cat << EOF
    TODO:

      - Write a console renderer

      - Write a terminal manual renderer!!

      - Write a template-based HTML renderer
EOF
}

articles.unused-code()
{
  python3 -m vulture src/articles.py
}



