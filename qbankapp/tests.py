from django.test import TestCase, Client
from mainapp.models import Maths, GeneralA
from .models_english import English


class QbankMathsTestCase(TestCase):

	@staticmethod
	def make_nth_record(n):
		#returns as (que, ch1, ch2, ch3, ch4, ans, wor, valid) 
		return (f'Maths Question {n}',
				n*4 -3, n*4 -2, n*4 -1, n*4,
				'A',
				f'Solution for Question {n}',
				True
		)

	@classmethod
	def setUpClass(cls):
		cls.client = Client()

	@classmethod
	def tearDownClass(cls):
		pass

	def setUp(self):
		for qnum in range(1,21):
			(que, ch1, ch2, ch3, ch4, ans, wor, valid) = self.make_nth_record(qnum)
			Maths.objects.create(que =que, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, ans=ans, wor=wor, valid=valid)

	def tearDown(self):
		Maths.objects.all().delete()

#### Test_create:
# Create 20 records
# Assert the record contents in  db
# Confirm non-null fields in the record
# Assert pk is in sequence
# Create a record 21 using the test client tool
	def test_create(self):
		self.assertEqual(Maths.objects.count(),20,msg=" Database count is not correct. 20 expected")
		fifth_rec = Maths.objects.filter(que__contains='Maths Question 5')[0]
		sixth_rec = Maths.objects.filter(que__contains='Maths Question 6')[0]
		self.assertEqual(fifth_rec.wor,'Solution for Question 5', msg='DB has incorrect Record. \
			5th Rec Expected')
		self.assertTrue(all(fifth_rec.to_dict()),msg='DB 5th record has null fields')
		self.assertEqual(fifth_rec.pk +1, sixth_rec.pk,msg='primary key out of sequence. 6 expected ')

		(que, ch1, ch2, ch3, ch4, ans, wor, valid) = self.make_nth_record(21)
		
		response = self.client.get('/qbank/create/maths')
		self.assertEqual(response.status_code, 200,'create page GET returned a failure html status code')
		response = self.client.post('/qbank/create/maths',{
			'que':que, 'ch1':ch1, 'ch2':ch2, 'ch3':ch3, 
			'ch4':ch4, 'ans':ans, 'wor':wor, 'valid':valid
		},follow=True)
		self.assertEqual(response.status_code, 200,'create page POST returned  html status code')
		twentyfirst_rec = Maths.objects.filter(que__contains='Maths Question 21')[0]
		self.assertEqual(twentyfirst_rec.wor,'Solution for Question 21', msg='DB has incorrect Record. \
			21th Rec Expected')


#### Test_update:
#create 20 records
#update the 11th records
#Assert the record contents in db
#Confirm non-null fields in the record
#update 19th record and confirm the pk is in sequence
	def test_update(self):
		eleventh_rec = Maths.objects.filter(ch4__contains=44)[0]
		self.assertEqual(eleventh_rec.que,'Maths Question 11', msg='DB has incorrect Record. \
			11th Rec Expected')
		eleventh_rec.que = 'Maths Question 11 updated'
		eleventh_rec.save()
		eleventh_rec = Maths.objects.filter(ch4__contains=44)[0]
		self.assertEqual(eleventh_rec.que,'Maths Question 11 updated', msg='DB update for 11th Rec failed')
		self.assertTrue(all(eleventh_rec.to_dict()), msg='DB 11th record has null fields')


		#(que, ch1, ch2, ch3, ch4, ans, wor, valid) = self.make_nth_record(21)
		response = self.client.get('/qbank/update/maths/pk=1')
		self.assertEqual(response.status_code,200,msg='update page GET returned a failure html status code')
		#ninteenth_rec = Maths.objects.filter(que__contains='Maths Question 19')[0]
		#print(ninteenth_rec.que)
	
		

#### Test_list:
#create 10 records
#check the  object list count passed to template is 10
#Assert that the href on qnumber points to the question update link
# read the 9th record from the webpage and assert it agains the database contents
	def test_list(self):
		pass

#### Test_FillDB:
#Read the test_data.xlsx file  with 20 records and polutate the db
#Assert the first record in the testfile with the first record in DB
#Assert the last record of the testfile with the  last element of the DB
#Assert the fifth record of the testfile with the 5th record of the DB
#Test Assertraise if test_data.xlsx is not present
#Test Assertraise if the model sheet is missing in test_data.xlsx
#Create a record in DB and assert that it is following the last record sequence
	def test_fill_data_base(self):
		pass
		
#### Test_BackUpDB:
#Read the test_data.xlsx file  with 20 records and polutate the db
#Backup the DB to test_bkp.xlsx file
#Assert the first record in the testbkpfile with the first record in DB
#Assert the last record of the testbkpfile with the  last element of the DB
#Assert the fifth record of the testbkpfile with the 5th record of the DB
#Create a new record in DB and assert that it is following the last record sequence
	def test_backup_database(self):
		pass
