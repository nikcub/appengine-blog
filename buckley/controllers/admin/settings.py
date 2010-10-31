
class Settings(reqhandlers.Admin):
	def get(self, val):
		settings = self.conf
		self.render('settings', {
			'settings': settings
		})
	def post(self):
		self.render_error('not yet implemented')



