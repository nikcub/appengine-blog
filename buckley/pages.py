import reqhandlers

class About(reqhandlers.Base):
  def get(self, path = None):
    return self.render('about', {'tab_about': True})

class Contact(reqhandlers.Base):
  def get(self, path = None):
    return self.render('contact', {'tab_contact': True})

class Consulting(reqhandlers.Base):
  def get(self, path = None):
    self.render('consulting', {'tab_consulting': True})