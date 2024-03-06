# import html

# from spans import Span


# def st(a, b):
#   return WebStyle(css={a: b})


# def cl(*a):
#   return WebStyle(classes=a)


# class WebStyle:
#   def __init__(self, classes=None, tag=None, css=None):
#     self.classes = set(classes) if classes else set()
#     self.tag = tag
#     self.css = css if css else {}

#   def __add__(self, other):
#     """ `other` overwrites `this` where applicable """
#     assert(isinstance(other, WebStyle))
#     classes = self.classes | other.classes
#     tag = other.tag if other.tag else self.tag
#     styles = dict(self.css)
#     styles.update(other.css)
#     return WebStyle(classes, tag, styles)

#   def __str__(self):
#     return str(self.__dict__)


# DefaultInlineStyletab = {
#   st.Bold:        st('font-weight','bold'),
#   st.Italic:      WebStyle(tag='em'),
#   st.Underline:   st('text-decoration', 'underline'),
#   st.Strike:      st('text-decoration', 'strikethrough'),
#   st.Subscript:   st('vertical-align', 'sub') + st('font-size', 'smaller'),
#   st.Superscript: st('vertical-align', 'super') + st('font-size': 'smaller'),
#   st.Smallcaps:   st('font-variant', 'small-caps'),
#   st.Var:         WebStyle(tag='code')
# }


# DefaultCSSClassTab = {
#   st.Bold:        cl('bold'),
#   st.Italic:      cl('italic'),
#   st.Underline:   cl('underlined'),
#   st.Strike:      cl('struck'),
#   st.Subscript:   cl('subscript'),
#   st.Superscript: cl('superscript'),
#   st.Smallcaps:   cl('smallcaps'),
#   st.Var:         cl('inline-var') + WebStyle(tag='code')
# }


# class SimpleHTMLRenderer(Handler):
#   HeaderTemplate = """
#   <!DOCTYPE html>
#   <html lang="en">
#   <head>
#     <meta charset="utf-8"/>
#     <title>{title}</title>
#     <link rel="stylesheet" href="tufte.css"/>
#     <meta name="viewport" content="width=device-width, initial-scale=1"/>
#   </head>"""
#   Heading = '<h{lvl} id="{id}">{text}</h{lvl}>'
#   BeginSection = '<section>'
#   EndSection = '</section>'
#   Paragraph = '<p>{}</p>'
#   Quote = '<blockquote><p>{}</p></blockquote>'
#   Code = '<code>{}</code>'
#   Pre = '<pre>{}</pre>'
#   Unknown = "<h3>Unknown Frame {kind}</h3><pre>{text}</pre>"
#   FooterTemplate = "</html>"


#   def __init__(self):
#     self.parts = []
#     self.sections = 0

#   def spanText(self, spans):
#     parts = []
#     for s in spans:

#       for style in s.style:
#         parts.append(f'<{style}>')

#       parts.append(s.text)

#       for style in s.style:
#         parts.append(f'</{s}>')

#     return ''.join(parts)

#   def renderBody(self, e):
#     k = e.kind

#     text = html.escape(self.spanText(e.spans))

#     if k == 'h':
#       self.next.handle(self.Heading.format(lvl=e.level, id=e.pid, text=text))

#     elif k == 'p':
#       self.next.handle(self.Paragraph.format(text))

#     elif k in set(('q', 'mn', 'in', 'fn', 'note')):
#       self.next.handle(self.Quote.format(text))

#     elif k == 'code':
#       self.next.handle(self.Code.format(text))

#     elif k == 'pre':
#       self.next.handle(self.Pre.format(text))

#     else:
#       self.next.handle(self.Unknown.format(kind=k, text=text))

#   def handle(self, article):
#     headerString = self.HeaderTemplate.format(title=article.title)
#     self.next.handle(headerString)

#     self.next.handle("<body><article>")
#     self.next.handle(f"<h1>{article.title}</h1>")

#     for sec in article.sections:
#       self.next.handle('<section>')
#       for element in sec.elements:
#         self.renderBody(element)
#       self.next.handle('</section>')


#     self.next.handle("</article></body></html>")

#   def finish(self):
#     self.next.finish()
