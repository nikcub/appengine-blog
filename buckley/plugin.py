from google.appengine.ext.webapp import template
import logging, os

class Plugin_base(object):
	
	_config = {}
	
	def __init__(self):
		# self.name = name
		if hasattr(self, 'initialize'):
			self.initialize('two')
	
	def set_config(self, config):
		if isinstance(config, dict):
			self._config = config
		else:
			logging.error('Could not set config for plugin %s' % self.__class__)
			return False
		
		return True
			
	def get_conf(self, val):
		if self._config.has_key(val):
			return self._config[val]
		else:
			return False
	
	def get_template_vars(self, vars):
		vars['conf'] = self._config
		return vars
		
	def render_template(self, vars):
		vars = self.get_template_vars(vars)
		try:
			content = template.render(self.get_template(), vars)
		except Exception, e:
			logging.exception('Could not render template: ' % e)
		return content
	
	def get_template(self, template_name = False):
		# plugin_name = self.__class__
		plugin_name = self.__class__.__name__
		path = os.path.join(os.path.dirname(__file__), 'plugins', plugin_name, plugin_name + '.html')
		
		if os.path.isfile(path):
			return path
		else:
			return False