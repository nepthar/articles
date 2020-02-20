

class Element:
  def __init__(self):
    self.text = None
    print("element init")

  def __str__(self):
    return f"<{self.__class__.__name__}>"


class Visible(Element):
  pass


class Invisible(Element):
  pass


class Comment(Invisible):
  def __init__(self, text):
    self.text = text


class Whitespace(Invisible):
  def __init__(self, count):
    self.count = count
    self.text = ''


class Unknown(Visible):
  def __init__(self, text):
    self.text = text


class Heading(Visible):
  def __init__(self, level, text):
    self.level = level
    self.text = text


class Paragraph(Visible):
  def __init__(self, text):
    self.text = text


class Blockquote(Visible):
  def __init__(self, lines):
    self.text = text
