import reqhandlers

class Consulting(reqhandlers.Base):
  def get(self, path):
    self.render('consulting', {})