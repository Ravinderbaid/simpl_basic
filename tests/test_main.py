import mock
from customer import User, Merchant
from transact import Transact
from reporting import Reporting
from main import main, create_user_or_merchant, create_new_transaction

class TestMain:
	def setup(self):
		self.report = Reporting()
		self.class_map = {
					"user" : {"class_name": User, "report_object": self.report.user_objects}, 
					"merchant" :{"class_name": Merchant, "report_object": self.report.merchant_objects},
					"txn": {"class_name": Transact, "report_object": self.report.transact_objects}, 
					"report" : {"class_name": Reporting, "report_object": self.report}
				}

	def test_main_create_new_user(self):
		input_type = self.class_map["user"]
		assert create_user_or_merchant("ravinder","ra@gmail.com",1000, input_type["report_object"], input_type["class_name"]) == "ravinder(1000)"	

	def test_main_create_new_user_negative(self):
		input_type = self.class_map["user"]
		try:
			create_user_or_merchant("ravinder","ra@gmail.com",1000, input_type["report_object"], input_type["class_name"])
			assert False
		except Exception as e:
			assert e.message == "User already exists"

	def test_main_create_new_user_name_format_negative(self):
		input_type = self.class_map["user"]
		try:
			create_user_or_merchant("r123","r@gmail.com",1000, input_type["report_object"], input_type["class_name"])
			assert False
		except Exception as e:
			assert e.message == "Name format invalid"
			
	def test_main_create_new_merchant(self):
		input_type = self.class_map["merchant"]
		assert create_user_or_merchant("merchant","ra@gmail.com",10, input_type["report_object"], input_type["class_name"]) == "merchant(10)"	

	def test_main_create_new_merchant_negative(self):
		input_type = self.class_map["merchant"]
		try:
			create_user_or_merchant("merchant","ra@gmail.com",10, input_type["report_object"], input_type["class_name"])
			assert False
		except Exception as e:
			assert e.message == "Merchant already exists"

	def test_main_create_new_merchant_name_format_negative(self):
		input_type = self.class_map["merchant"]
		try:
			create_user_or_merchant("m123","r@gmail.com",1000, input_type["report_object"], input_type["class_name"])
			assert False
		except Exception as e:
			assert e.message == "Name format invalid"
	
	@mock.patch("simpl.transact.Transact.check_transact", return_value= "1")
	def test_create_new_transaction_positive(self, mock_check_transct):
		input_type = self.class_map["txn"]
		assert create_new_transaction(self.class_map["user"]["report_object"].get("ravinder"),
								self.class_map["merchant"]["report_object"].get("merchant"),
								input_type["report_object"],
								input_type["class_name"],
								1000
								) == "success"

	@mock.patch("simpl.transact.Transact.check_transact", return_value= "0reason : Credit limit")
	def test_create_new_transaction_negative_credit_limit(self, mock_check_transct):
		input_type = self.class_map["txn"]
		assert create_new_transaction(self.class_map["user"]["report_object"].get("ravinder"),
								self.class_map["merchant"]["report_object"].get("merchant"),
								input_type["report_object"],
								input_type["class_name"],
								1000
								) == "rejected : reason : Credit limit"

	@mock.patch("simpl.main.create_user_or_merchant",return_value="ravinder(1000)")
	def test_main_create_user(self, mock_create_user):
		assert main("new user ravinder ra@gmail.com 10000", self.class_map) == "ravinder(1000)"

	def test_main_create_user_negative(self):
		try:
			main("new user ravinder baid ra@gmail.com 10000", self.class_map)
			assert False
		except Exception as e:
			assert True

	@mock.patch("simpl.main.create_new_transaction",return_value="success")
	def test_main_create_transcation(self, mock_check_transct):
		assert main("new txn ravinder merchant 1000", self.class_map) =="success"
	
	def test_main_create_transcation_wrong_merchant(self):
		try:
			main("new txn ravinder merchant123 1000", self.class_map)
			assert False
		except Exception as e:
			assert True
	
	def test_main_create_transcation_wrong_user(self):
		try:
			main("new txn ravinderqww merchant 1000", self.class_map)
			assert False
		except Exception as e:
			assert True
	
	def test_main_create_transcation_wrong_input(self):
		try:
			main("new 123 ravinderqww merchant 1000", self.class_map)
			assert False
		except Exception as e:
			assert True
	
	@mock.patch("simpl.customer.Merchant.update_discount", return_value = True)
	def test_main_create_update(self, mock_update_discount):
		assert main("update merchant merchant 10", self.class_map) == True

	def test_main_create_update_negative(self):
		try:
			main("update merchant masdasda 10", self.class_map)
			assert False
		except Exception as e:
			assert True

	@mock.patch("simpl.customer.User.check_limit", return_value=0.0)
	@mock.patch("simpl.customer.User.update_limit", return_value=True)
	def test_main_payback_positive(self, mock_check_limit, mock_update_limit):
		assert main("payback ravinder 1000", self.class_map) == "ravinder(dues:0.0)"
	
	@mock.patch("simpl.customer.User.update_limit", return_value=False)
	def test_main_payback_negative_limit(self, mock_update_limit):
		try:
			main("payback ravinder 1000", self.class_map)
			assert False
		except Exception as e:
			assert True

	def test_main_payback_negative_user(self):
		try:
			main("payback ravi 1000", self.class_map)
			assert False
		except Exception as e:
			assert True

	@mock.patch("simpl.reporting.Reporting.total_discount_merchant", return_value=6.25)
	def test_main_report_discount(self, mock_total_discount_merchant):
		assert main("report discount merchant", self.class_map) == 6.25

	@mock.patch("simpl.customer.User.check_limit", return_value=100.27)
	def test_main_report_user(self, mock_total_discount_merchant):
		assert main("report dues ravinder", self.class_map) == 100.27

	def test_main_report_user_negative(self):
		try:
			main("report dues ravinderassdas", self.class_map)
			assert False
		except Exception as e:
			assert True
	
	@mock.patch("simpl.reporting.Reporting.users_at_credit_limit", return_value="ravinder")
	def test_main_report_users_at_credit_limit(self, mock_users_at_credit_limit):
		assert main("report users-at-credit-limit", self.class_map) == "ravinder"

	@mock.patch("simpl.reporting.Reporting.dues_user", return_value=300)
	def test_main_report_total_dues(self, mock_total_discount_merchant):
		assert main("report total-dues", self.class_map) == "total: 300"


	def test_main_report_negative(self):
		try:
			main("report 123 ravinderassdas", self.class_map)
			assert False
		except Exception as e:
			assert True

	def test_main_report_index_negative(self):
		try:
			main("new user ravinderassdas", self.class_map)
			assert False
		except Exception as e:
			assert True

	def test_main_report_input_negative(self):
		try:
			main("asbsd users ravinderassdas", self.class_map)
			assert False
		except Exception as e:
			assert True
