from django.test import TestCase
from selenium import webdriver

from .models import Maths,English,GeneralA

class ModelTest(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.browser = webdriver.Chrome()
		cls.browser.get('http://127.0.0.1:8000/')

	@classmethod
	def tearDownClass(cls):
		cls.browser.quit()

	def test_maths(self):
		maths_obj = Maths()
		self.assertEqual(str(maths_obj), f"Maths: Question Number - {maths_obj.pk}")

	def test_english(self):
		english_obj = English()
		self.assertEqual(str(english_obj), f"English: Question Number - {english_obj.pk}")

	def test_generala(self):
		generala_obj = GeneralA()
		self.assertEqual(str(generala_obj), f"GeneralA: Question Number - {generala_obj.pk}")

	def test_homepage(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertIn('Home', self.browser.title)