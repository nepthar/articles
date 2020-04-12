#!/usr/bin/env bash

ws_name="articles"

# This file is designed to work with Nepthar's shell tools, but it
# can be used without them. See https://github.com/nepthar/shtools
# Functions prefixed here with "articles." should be run from the
# project root


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
  - Merge framing and decoding. Unfortunately, you have to because of the two
    consecutive section titles problem :(

  - Write a console renderer

  - Write a template-based HTML renderer
EOF
}

articles.unused-code()
{
  python3 -m vulture src/articles.py
}



