#!/usr/bin/env bash

ws_name="article"

# This file is designed to work with Nepthar's shell tools, but it
# can be used without them. See https://github.com/nepthar/shtools

# Common workspace commands:

article.json-sample()
{
  python3 src/articles.py -json ./samples/paragraphs.article
}
