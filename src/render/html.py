class HtmlHeader:
  Charset = 'utf-8'
  Lang = 'en'

  def __init__(self, title=None):
    self.title = title
    self.meta = {}
    self.links = []
    self.scripts = []

  def link(where, type=None, rel=None):
    raise NotImplementedError()

  def meta(key, value):
    self.meta.append({'name': key, 'content': value})

#   def script(url,



# class HtmlBuilder:

#   Lang = 'en'

#   def __init__(self, title):
#     self.meta = []
#     self.body = []
#     self.feets = []



