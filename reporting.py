class Reporting:
	"""
	Used this class as a utility where I could store all the user,merchant, transcation objects
	"""
	def __init__(self,user_objects={},merchant_objects={},transact_objects={}):
		self.user_objects = user_objects
		self.merchant_objects = merchant_objects
		self.transact_objects = transact_objects

	def total_discount_merchant(self,merchant):
		#total discount given by the merchant
		total_discount = 0
		for transact in self.transact_objects:
			if self.transact_objects[transact].merchant.get_name() == merchant and self.transact_objects[transact].status:
				total_discount+=self.transact_objects[transact].amount*float(self.transact_objects[transact].merchant.discount/100)
		return total_discount

	def dues_user(self):
		#total dues of a user or all the user
		total = 0
		for user in self.user_objects: 
			due = self.user_objects[user].check_limit()
			if due:
				print("{}: {}".format(user,due))
				total+=due
		return total

	def users_at_credit_limit(self):
		#show users at credit limit
		users = []
		for user in self.user_objects:
			if self.user_objects[user].current_limit == 0.0:
				users.append(user)
		if users:
			return "\n".join(user for user in users)
		else:
			return None
