from customer import User, Merchant, Customer
from exception import EmailException, NameException, ValidDiscountException

class TestClassCustomer:
	def setup(self):
		self.new_customer = Customer()
		
	def test_customer_email(self):
		self.new_customer.set_email("ravinder@simpl.com")
		assert self.new_customer.get_email() == "ravinder@simpl.com"

	def test_customer_email_negative(self):
		try:
			self.new_customer.get_email()
			assert False
		except Exception:
			assert True

	def test_customer_set_email(self):
		assert self.new_customer.set_email("ravinder@simpl.com") == None

	def test_customer_set_email_negative(self):
		try:
			self.new_customer.set_email("r@s.com")
			assert False
		except EmailException as e:
			assert e.message == "Email format invalid"

	def test_customer_name(self):
		self.new_customer.set_name("ravinder")
		assert self.new_customer.get_name() == "ravinder"

	def test_customer_name_negative(self):
		try:
			self.new_customer.get_name()
			assert False
		except Exception:
			assert True

	def test_customer_set_name(self):
		assert self.new_customer.set_name("ravinder") == None

	def test_customer_set_email_name(self):
		try:
			self.new_customer.set_name("rdasda12323")
			assert False
		except NameException as e:
			assert e.message == "Name format invalid"
	
	def test_customer_create(self):
		self.new_customer.create("ravinder","ravinder@simpl.com")
		assert self.new_customer.get_name() == "ravinder"
		assert self.new_customer.get_email() == "ravinder@simpl.com"

	def test_customer_create_negative(self):
		try :
			self.new_customer.create("ravinasdasd12213123der","ravinder@simpl.com")
			assert False
		except NameException as e:
			assert e.message == "Name format invalid"
		try:
			self.new_customer.create("ravinder","r123@s123.com")
		except EmailException as e:
			assert e.message == "Email format invalid"

class TestUser:
	
	def setup(self):
		self.new_user = User(1000)
	
	def test_user_checklimit(self):
		assert self.new_user.check_limit() == 0.0

	def test_user_updatelimit_after_update(self):
		self.new_user.update_limit(-100)
		assert self.new_user.check_limit() == 100.0

	def test_user_updatelimit_after_update_positive(self):
		self.new_user.update_limit(100)
		assert self.new_user.check_limit() == 0.0		

	def test_user_updatelimit_positive(self):
		assert self.new_user.update_limit(-100) == 1

	def test_user_updatelimit_negative(self):
		print(self.new_user.current_limit)
		assert self.new_user.update_limit(10000) == 0


class TestMerchant:
	
	def setup(self):
		self.new_merchant = Merchant(1.25)
	
	def test_update_discount_positive(self):
		old_discount = self.new_merchant.discount
		assert self.new_merchant.update_discount(10) == "Updated discount from {}% to {}%".format(old_discount,10)

	def test_update_discount_negative(self):
		try:
			self.new_merchant.update_discount(0)
			assert False
		except ValidDiscountException as e:
			assert e.message == "Invalid discount, discount cannot be less than 0"
