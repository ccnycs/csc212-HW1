import unittest
from os.path import exists as file_exists
import os
from yaml import safe_load
from subprocess import Popen, PIPE
import math
import sys
import traceback
import glob
import random
import string

import pexpect
from pexpect import ExceptionPexpect

STUDENT_CODE_NAME = 'main.cpp'

def randstr():
	return "".join(random.sample(string.ascii_letters, random.randint(10,20)))


def get_actual(child, ind):
	output = child.before.split("\n")
	if len(output)<=math.fabs(ind):
		return ""
	return output[ind].strip()


class SolutionError(Exception):
	def __init__(self, params):
		sys.tracebacklimit=0
		self.__context__ = None
		self.params = params
		
	def __str__(self):
		msg = "\n".join(["{testname} Test",
		                 "Input: {input}",
						 "Correct Answer: {expected}", 
						 "Given Answer: {actual}"])
		return msg.format(**self.params)
						
	def __repr__(self):
		return self.__str__()
						
class TestProblem1(unittest.TestCase):
    @classmethod
    def setUp(self):
        return  
      
    def tearDown(self):
        pass

    def test_binary_exists(self):
	yes = os.path.exists(os.path.join(os.getcwd(), 'student'))
	self.assertTrue(yes)
		
	#4 points
    def test_output(self):
	"""Tests outputs correct"""
	child = pexpect.spawn('./student')
		
	input = ""
	expected = "What is your name?"
	try:
		child.expect(expected)
	except ExceptionPexpect as e:
		params = {'testname': "Given output correct",
			  'input': input,
			  'expected': expected, 
                          'actual': get_actual(child,0)}
		raise SolutionError(params)

	input = randstr()
	expected = "Hello \w+!"
	try:
		child.sendline(input)
		child.expect(expected)
	except ExceptionPexpect as e:
		params = {'testname': "Verbatim Output",
		          'input': input, 
			  'expected': expected, 
			  'actual': get_actual(child,1)}
		raise SolutionError(params)
    
    #6 points
    def test_input_output(self):
        """Replaces Name Properly"""
	child = pexpect.spawn('./student') 
	child.expect(".")
	name = randstr()
	expected = "Hello {}!".format(name)
	try:
		child.sendline(name)
		child.expect(expected)
	except ExceptionPexpect as e:
		params = {'testname': "Print Name", 
			  'input': input, 
			  'expected': expected, 
			  'actual': get_actual(child,1)}
		raise SolutionError(params)
                                                                    
          
if __name__ == '__main__':
    unittest.main()

