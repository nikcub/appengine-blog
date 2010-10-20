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