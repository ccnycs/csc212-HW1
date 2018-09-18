import math
from pathlib import Path
import random
import string
import sys
import traceback

import pexpect
from pexpect import ExceptionPexpect

import pytest

def test_binary_exists():
    p = Path(Path.cwd()/'main')
    assert p.exists()
    
class TestIO(object):
    
    output_1 = "What is your name?"
    output_2 = "Hello {}"
    executable = './main'
    
    
    def test_output(self):
        """Tests outputs correct"""
        child = pexpect.spawn(TestIO.executable)        
        try:
            child.expect(TestIO.output_1)
        except ExceptionPexpect as e:
            params = error("Test Prompt", " ",
                           TestIO.output_1, child, 0)
            raise SolutionError(params)
        
        name = "world!"
        try:
            child.sendline(name)
            child.expect(TestIO.output_2.format(name))
        except ExceptionPexpect as e:
            params = error("Test Output", name,
                           TestIO.output_2.format(name), child, 1) 
            raise SolutionError(params)
    
        #6 points
        def test_input_output(self):
            child = pexpect.spawn(TestIO.executable)
            child.expect(".")
            letters = random.sample(string.ascii_letters,
                                    random.randint(9,20))
            name = "".join(letters)
            try:
                child.sendline(name)
                child.expect(TestIO.output_2.format(name))
            except ExceptionPexpect as e:
                params = error("Print Name", name,
                               TestIO.output_2.format(name), child, 1)
                raise SolutionError(params)

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

def error(testname, name, exp, child, ind):
    output = str(child.before).split("\n")
    if len(output)<=math.fabs(ind):
        test_out = ""
    else:
        test_out = output[ind].strip()
    return {'testname':testname,'input': name,
            'expected': exp, 'actual': test_out}
