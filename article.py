from src.articles import *
from src.elements import *

def l(text, src):
  return Span(text, link=src)

def s(thing):
  if isinstance(thing, Span):
    return [thing]
  if isinstance(thing, list):
    return thing
  if isinstance(thing, str):
    return [Span(thing)]

def p(spans):
  e = ParagraphElement(s(spans))
  return e

def h1(spans):
  e = HeadingElement(s(spans), 1)
  return e

def h2(spans):
  e = HeadingElement(s(spans), 2)
  return e


def tufte_css():
  a = Article()
  a.meta = {
    'charset': 'utf-8',
    'title': 'Tufte CSS',
    'lang': 'en'
  }

  a.body = [
    h1(s('Tufte CSS')),
    h2(s('Dave Liepmann')),
    p('Tufte CSS provides tools to style web articles using the ideas demonstrated by Edward Tufte’s books and handouts. Tufte’s style is known for its simplicity, extensive use of sidenotes, tight integration of graphics with text, and carefully chosen typography.'),
    p([
      s('Tufte CSS was created by'),
      l('Dave Liepmann', 'http://www.daveliepmann.com'),
      s(' and is now and Edward Tufte project. The original idea was cribbed from ')
      ])
  ]
