from django.test import TestCase
from django.urls import reverse
from .forms import ParamForm
# Create your tests here.

# views (uses selenium)

import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
#driver = webdriver.Firefox(executable_path=r'your\path\geckodriver.exe')
'''
class Testinput(LiveServerTestCase):
    port=8000

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_input_fire(self):
        self.driver.get("http://localhost:8000/grapher/")
        self.driver.find_element_by_name('temperature').send_keys('0.1')
        self.driver.find_element_by_name('radius').send_keys('1e12')
        self.driver.find_element_by_name('redshift').send_keys('0.03')
        self.driver.find_element_by_xpath("//input[@name='redshift']").submit();
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "tester")))
        finally:
            self.driver.quit()
        self.assertIn("http://localhost:8000/", self.driver.current_url)

        #self.driver.find_element_by.tagName("input").submit()
    def tearDown(self):
        self.driver.quit


'''


class Formtest(TestCase):
    def test_forms_normal_input_true(self):
        form_data = {'temperature': 0.1, 'radius':0.1, 'redshift':0.1}
        form = ParamForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_forms_formerrors_true(self):
        response = self.client.post(ParamForm(), {'temperature': 0.1, 'radius':0.1})
        self.assertFormError(response, ParamForm(), 'redshift', 'This field is required.')

