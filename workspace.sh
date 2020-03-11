#!/usr/bin/env bash

ws_name="articles"

# This file is designed to work with Nepthar's shell tools, but it
# can be used without them. See https://github.com/nepthar/shtools

articles.todo() {
  cat << EOF
TODO:
  - Make the "Article" class
  - Figure out how renderers will work
  - Write a simple HTML renderer
  - Write a console renderer
  - Write a template-based HTML renderer
EOF
}

articles.unused-code()
{
  python3 -m vulture src/articles.py
}



