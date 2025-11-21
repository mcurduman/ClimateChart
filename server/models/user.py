class User:
	def __init__(self, user_id: str, name: str, email: str, password: str, email_verified: bool = False):
		self.user_id = user_id
		self.name = name
		self.email = email
		self.password = password
		self.email_verified = email_verified

	def to_dict(self):
		return {
			"user_id": self.user_id,
			"name": self.name,
			"email": self.email,
			"password": self.password,
			"email_verified": self.email_verified,
		}
