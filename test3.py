from selenium import webdriver
from selenium import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time

url = "https://www.fazzaco.com/awards/Fazzaco-business-awards-2022-voting-for-companies"


class Process:

	driver = None

	def __init__(self,url):	
		try:
			self.options = Options()
			self.options.headless = False
			self.options.add_argument('--start-maximized')
			self.driver = webdriver.Chrome(options=self.options)
			
			self.action = ActionChains(self.driver)
			
			self.url = url
			# print(dir(self.driver))
			self.driver.get(url)

			self.company_name_class = "company-voting__name"
			self.vote_login_class = "vote-login"
			self.vote_btn_class = "vote-login-btn_sure"
			self.vote_input_class = "vote-popup__input"
			self.company_div_class = "company-voting"
			self.test_email = "praiseike123@gmail.com"
			self.test_name = "David Bassey"

			self.target_company = "Alpari"
			self.target_company_div = None

			# self.driver.execute_script("document.body.style.zoom=50%;")

			self.run()

		except Exception as exception:
			self.quit()
			print(exception)


	def castVote(self,target_company_vote_btn,company_name):
		vote_login_div = self.driver.find_element_by_class_name(self.vote_login_class)
		name_field,email_field = vote_login_div.find_elements_by_class_name(self.vote_input_class)
		name_field.send_keys(self.test_name)
		email_field.send_keys(self.test_email)
		vote_login_btn = vote_login_div.find_element_by_class_name(self.vote_btn_class)
		self.driver.execute_script('arguments[0].click()',vote_login_btn)
		time.sleep(2)
		# target_company_vote_btn.click()
		self.action.move_to_element(self.company_div)
		self.driver.execute_script('arguments[0].click()',target_company_vote_btn)
		self.driver.execute_script('arguments[0].click()',target_company_vote_btn)
		print("Voted:",company_name)


	def quit(self):
		if self.driver is not None:
			self.driver.quit();
			quit()


	def run(self):
		try:
			foundTarget = False;
			self.driver.execute_script("window.scrollBy(0,2200)")
			while not foundTarget:
				company_divs = self.driver.find_elements_by_class_name(self.company_div_class)
				for company_div in company_divs:		
					company_name = company_div.find_element_by_class_name(self.company_name_class);
					company_name = company_name.get_attribute('innerText')
					if company_name.lower().strip() == self.target_company.lower().strip():
						print("Found Target:",company_name)
						self.company_div = company_div
						target_company_vote_btn = company_div.find_element_by_class_name('company-voting__vote-btn-box')
						self.driver.execute_script('arguments[0].click()',target_company_vote_btn)
						self.action.move_to_element(company_div).perform()
						# self.driver.execute_script('window.scrollTo(0,arguments[0].offsetTop)',company_div)
						time.sleep(1)
						self.castVote(target_company_vote_btn,company_name)
						foundTarget = True;
						break;
				if not foundTarget:
					self.driver.execute_script("window.scrollBy(0,300);")
					time.sleep(1)

		except Exception as e:
			print("Error:",e)


		time.sleep(3)
		self.quit()

	def __del__(self):
		time.sleep(2)




app = Process(url)
print("Done")