
class Group(db.Model):
	name = db.StringProperty()
	
	
class Membership(db.Model):
	user = db.ReferenceProperty(User)
	group = db.ReferenceProperty(Group)
	group_name = db.StringProperty()
	
	def put(self):
		self.group_name = self.group.name
		super(Membership, self).put()
	
	def get_group(self, name):
		return [n.group for n in user.membership_set.order('group_name')]
		
	@classmethod
	def create(username, groupname):
		Super(Membership, user = username, group = groupname).put()
		# Membership.get_or_insert(key_name = "%s-%s" % (user.key(), group.key()), user = user, group = group).put()
		
		
	