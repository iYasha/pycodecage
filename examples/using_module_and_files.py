from pycodecage import BuiltinsFactory, TrustedEnvironment, FileFactory, TestCase, run_tests
import re

code = """
import re

def find_numbers(filename):
    with open(filename, 'r') as file:
        text = file.read()
        return re.findall(r'\d+', text)

numbers = find_numbers('example.txt')
print(numbers)
"""

builtins = BuiltinsFactory([re])
builtins.update('open', FileFactory({'example.txt': 'asdfjkafsjkl@$123125ASDjkfajls 14'}))
env = TrustedEnvironment(code, builtins)
tests = [
    TestCase('test1', [], ["['123125', '14']"]),
]
run_tests(tests, env)
