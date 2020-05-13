class Transact:
	transact_count=0
	def __init__(self, user, merchant, amount, transact_type):
		self.user = user
		self.merchant = merchant
		self.amount = float(amount)
		self.transact_type = transact_type
		self.status = 0
	
	def validate_amount(self):
		#validate if amount used for transaction is not negative
		if self.amount<=0:
			return 0
		return 1

	def check_transact(self):
		#check and perform transaction if valid
		reason = ""
		if self.validate_amount():
			if self.user.current_limit>=self.amount:
				#As it is withdrawal so multiplied -1 * total amount as update limit would add all the amounts
				self.user.update_limit(-1*self.amount)
				self.status = 1
			else:
				reason = "reason : Credit limit"
		else:
			reason = "reason : Invalid amount"
		
		return str(self.status) +reason