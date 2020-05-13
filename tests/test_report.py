from customer import User, Merchant
from transact import Transact
from reporting import Reporting
import mock

class TestClassReport:
	def setup(self):
		l='abc'
		self.report = Reporting()
		self.empty_report = Reporting()
		for i in range(1,4):
			user = User(100*i)
			self.report.user_objects["alice"+l[i-1]] = user
			user.create("alice"+l[i-1],"alice@simpl.com")
			merchant = Merchant(1.25+float(i))
			self.report.merchant_objects["jack"+l[i-1]] = merchant
			merchant.create("jack"+l[i-1],"jack@simpl.com")
			transact = Transact(user,merchant,100,"withdrawl")
			self.report.transact_objects[i] = transact
			transact.check_transact()
	
	def test_total_discount_merchant(self):
		assert self.report.total_discount_merchant("jacka") == 2.25
		assert self.report.total_discount_merchant("jackb") == 3.25
		assert self.report.total_discount_merchant("jackc") == 4.25

	def test_dues_user(self):
		assert self.report.dues_user() == 300.0

	def test_users_at_credit_limit(self):
		assert self.report.users_at_credit_limit() == "alicea"

	def test_dues_user_empty(self):
		self.empty_report.user_objects = []
		assert self.empty_report.users_at_credit_limit() == None
