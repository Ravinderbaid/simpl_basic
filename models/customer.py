import re
from customexceptions.exception import NameException, EmailException, ValidDiscountException

class Customer:
	def __init__(self, name, email):
		self.name = name
		self.email = email

	@name.setter
	def name(self,name):
		if not re.match(r'[a-zA-Z]+$', name): 
			raise NameException("Name format invalid")
		self._name = name

	@property
	def name(self):
		return self._name

	@email.setter
	def email(self,email):
		if not re.match(r'^[a-zA-Z]{2,}@[a-zA-Z]{3,}.[a-z]{2,3}$', email): 
			raise EmailException("Email format invalid")
		self._email = email

	@property
	def email(self):
		return self._email

	# def create(self,name,email):
	# 	try:
	# 		self.set_name(name)
	# 		self.set_email(email)
	# 	except NameException:
	# 		print("Unable to set name as this is not a valid name, name may only consist of letter")
	# 		raise
	# 	except EmailException:
	# 		print("Unable to set email as this is not a valid email, email of format [<more_than_two_letter>@<more_than_three_letter>.<not_more_than_two_to_three_letter>]+(*All in small case)")
	# 		raise

class User(Customer):
	# user_count = 0 #Can be used to maintain id of similar merchants
	def __init__(self,name,email, limit):
		super.__init__(name,email)
		if float(limit) < 1:
			raise ValueError("Limit cannot be less than 1")
		self.limit=float(limit)
		self.current_limit=float(limit)
	
# 	def check_limit(self):
# 		#function to check current limit
# 		return self.limit-self.current_limit

# 	def update_limit(self, amount):
# 		#function to update current available limit on payback and transaction
# 		self.current_limit+=amount
# 		if self.current_limit > self.limit:
# 			self.current_limit-=amount		
# 			return 0
# 		return 1

class Merchant(Customer):
	# merchant_count = 0 #Can be used to maintain id of similar merchants
	def __init__(self, name, email, discount):
		super.__init__(name,email)
		if float(discount)< 0:
			raise ValueError("Discount cannot be less than zero")
		self.discount = float(discount)
	
# 	def update_discount(self, discount):
# 		#function to update the discount
# 		previous_discount = self.discount
# 		if discount>0:
# 			self.discount= discount 
# 			return str("Updated discount from {}% to {}%".format(previous_discount,self.discount))
# 		raise ValidDiscountException("Invalid discount, discount cannot be less than 0")
# 	

if __name__ == '__main__':
	inp = raw_input("User")
	inp  =  inp.split(" ")
	User(inp[0],inp[1],inp[2])

	inp = raw_input("Merchant")
	inp  =  inp.split(" ")
	User(inp[0],inp[1],inp[2])