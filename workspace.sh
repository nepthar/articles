#!/usr/bin/env bash

ws_name="articles"

# This file is designed to work with Nepthar's shell tools, but it
# can be used without them. See https://github.com/nepthar/shtools

# Common workspace commands:

articles.of()
{
  python3 src/articles.py < "$1"
}
