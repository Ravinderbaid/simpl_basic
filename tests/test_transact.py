import mock
from customer import User, Merchant
from transact import Transact

class TestTransactClass:
	def setup(self):
		user = User(100)
		user.create("alice","alice@simpl.com")
		merchant = Merchant(10)
		merchant.create("jack","jack@simpl.com")
		self.new_transact = Transact(user,merchant,100,"withdrawl")
		self.new_error_tranasct = Transact(user,merchant,-1000.0,"withdrawl")
		
	def test_validate_amount(self):
		assert self.new_transact.validate_amount() == 1
		assert self.new_error_tranasct.validate_amount() == 0

	@mock.patch("simpl.transact.Transact.validate_amount", return_value=True)
	def test_check_transact_positive(self, mock_validate_amount):
		assert self.new_transact.check_transact() == "1"

	@mock.patch("simpl.transact.Transact.validate_amount", return_value=False)
	def test_check_transact_negative_invalid_amount(self, mock_validate_amount):
		assert self.new_transact.check_transact() == "0reason : Invalid amount"

	def test_check_transact_negative_credit_limit(self):
		self.new_transact.user.current_limit = 0
		assert self.new_transact.check_transact()=="0reason : Credit limit"