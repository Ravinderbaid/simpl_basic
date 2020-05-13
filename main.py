from customer import User, Merchant
from transact import Transact
from reporting import Reporting

def create_user_or_merchant(name, email, value, customer_object, class_name):
	"""
	name				- name of user or merchant
	email 				- email of user or merchant
	value				- discount, limit in respect to merchant and user
	customer_objects 	- report object of to store object of type User or Merchant
	class_name			- name of class whose object would be create i.e. User or Merchant
	"""
	if not customer_object.get(name):
		#create a user,merchant object
		customer_object[name] = class_name(value)
		try:
			#add there name email and validate them
			customer_object[name].create(name,email)
		except Exception as e:
			del customer_object[name]
			raise
		return "{}({})".format(name, value)
	else:
		raise Exception("{} already exists".format(str(class_name.__name__)))

def create_new_transaction(user_name, merchant_name, transact_object, transact_class, amount):
	"""
	user_name			- User class object
	merchant_name		- Merchant class object
	transact_object 	- Report object to store object of type transact
	transact_class		- Name of class whose object would created 'Transact'
	amount				- Amount to be invloved in transaction
	"""
	
	Transact.transact_count+=1
	#create a new transaction object when valid user and merchant is there
	transact_object[Transact.transact_count] = transact_class(user_name, merchant_name, amount, "withdraw")
	#check if transcation is successful or not
	transaction=transact_object[Transact.transact_count].check_transact()
	if transaction[0] == "1":
		return "success"
	else:
		return "rejected : "+transaction[1:]
					

def main(current_input, class_map):
	current_input = current_input.split(" ")
	try:
		if current_input[0] == "new":
			if len(current_input) >5:
				raise Exception("Extra input given")
			#part of code to create a new user,merchant or transaction.
			class_type,name = current_input[1],current_input[2]
			if class_type in ["user", "merchant"]:
				return create_user_or_merchant(name,
												current_input[3], 
												current_input[4], 
												class_map[class_type]["report_object"],
												class_map[class_type]["class_name"]
												)	
	
			elif class_type == "txn":
				#create a new transaction
				merchant_name = current_input[3]
				if class_map["merchant"]["report_object"].get(merchant_name): #validate existing merchant
					if class_map["user"]["report_object"].get(name): #validate existing user
						return create_new_transaction(class_map["user"]["report_object"].get(name),
														class_map["merchant"]["report_object"].get(merchant_name),
														class_map[class_type]["report_object"],
														class_map[class_type]["class_name"],
														current_input[4]
														)
					else:
						raise Exception("Invalid user") 
				else:
					raise Exception("Invalid merchant") 
				
			else:
				# raise exception if any invalid input with new as prefix
				raise Exception("invalid Input")

		elif current_input[0] == "update":
			#update merchant discount
			name,discount = current_input[2],float(current_input[3])
			if class_map["merchant"]["report_object"].get(name):
				return class_map["merchant"]["report_object"][name].update_discount(float(discount))
			else:
				raise Exception("Invalid Merchant")

		elif current_input[0] == "payback":
			#update limit of user if they payback
			name,amount = current_input[1],float(current_input[2])
			if class_map["user"]["report_object"].get(name):
				if class_map["user"]["report_object"][name].update_limit(amount):
					return "{}(dues:{})".format(name, class_map["user"]["report_object"][name].check_limit())
				else:
					raise Exception("Payback amount greater than allocated limit")
			else:
				raise Exception("Invalid user")

		elif current_input[0] == "report":
			#used only to get reports
			report_type = current_input[1]
			reporting_object =  class_map['report']['report_object']
			if report_type == "discount":
				#call total_discount_merchant of class Reporting which would return total discount given till date by the merchant
				return reporting_object.total_discount_merchant(current_input[2])
			
			elif report_type == "dues":
				#get the total dues fof the asked user
				user_object = class_map['user']["report_object"]
			
				if user_object.get(current_input[2]): #validate for the user
					return user_object[current_input[2]].check_limit()
				else:
					raise Exception("Invalid user, user not present")
			
			elif report_type == "users-at-credit-limit":
				return reporting_object.users_at_credit_limit()
			
			elif report_type == "total-dues":
				return "total: {}".format(reporting_object.dues_user())
			
			else:
				raise Exception("Invalid input")
		else:
			raise Exception("Invalid input")
	except IndexError as e:
		return ("Expected more data {}".format(e.message))
	except Exception as e:
		return ("Error occured {}".format(e.message))
	
if __name__ == '__main__': #pragma: no cover
	report = Reporting()
	"""
	class_map is kind of config where we could put all the classes all the available objects of the respective classes
	"""
	class_map = {
					"user" : {"class_name": User, "report_object": report.user_objects}, 
					"merchant" :{"class_name": Merchant, "report_object": report.merchant_objects},
					"txn": {"class_name": Transact, "report_object": report.transact_objects}, 
					"report" : {"class_name": Reporting, "report_object":report}
				}

	while True:
		current_input = raw_input()
		if not current_input:
			break
		print(main(current_input, class_map))
