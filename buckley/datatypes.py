import re
from google.appengine.ext import db
from google.appengine.api import datastore_types
from vendor import markdown

Text = datastore_types.Text

class HtmlFromMarkdownProperty(db.TextProperty):
    def __init__(self, source=None, **kwargs):
        if not isinstance(source, db.TextProperty):
            raise TypeError('Source must be a TextProperty.')
        self.source = source
        super(HtmlFromMarkdownProperty, self).__init__(**kwargs)

    def get_value_for_datastore(self, model_instance):
        value = self.source.get_value_for_datastore(model_instance)
        if value is not None:
            html = markdown.markdown(value)
            return Text(html)

class StubFromTitleProperty(db.StringProperty):
	def __init__(self, source=None, **kwargs):
		if not isinstance(source, db.StringProperty):
			raise TypeError('Source must be a StringProperty.')
		self.source = source
		super(StubFromTitleProperty, self).__init__(**kwargs)

	def slugify(self, value):
		value = re.sub('[^\w\s-]', '', value).strip().lower()
		return re.sub('[-\s]+', '-', value)
		
	def get_value_for_datastore(self, model_instance):
		value = self.source.get_value_for_datastore(model_instance)
		if value is not None:
			stub = self.slugify(value)
			return Text(stub)

	def get_stub(self, title, inc = 1):
		stub_exists = Post.stub_exists(self.slugify(title))
		if stub_exists == False:
			return self.slugify(title)
		else:
			inc = inc + 1
			if inc > 2:
				return self.get_stub("%s-%d" % (self.slugify(title[:-2]), inc), inc)
			else:
				return self.get_stub("%s-%d" % (self.slugify(title), inc), inc)
