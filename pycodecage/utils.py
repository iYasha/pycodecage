from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pycodecage.test_case import TestCase
    from pycodecage.environment import TrustedEnvironment


def _import(name, *args, **kwargs):
    if name not in args[0]['__builtins__'] or name not in args[1]['__builtins__']:
        raise ImportError(f'No module named {name}')
    return __import__(name, *args, **kwargs)


class FileMock:
    _files = {}

    def __init__(self, name: str, mode: str = 'r', encoding: str = None, newline: str = '\n'):
        self.name = name
        if mode not in ('r', 'w', 'a', 'x', 'r+', 'w+', 'a+', 'x+'):
            raise ValueError(f'Invalid mode: {mode}')
        self.mode = mode
        self.encoding = encoding
        self.newline = newline
        self._closed = False
        self.__read_line_no = 0

    def write(self, text: str):
        if self._closed:
            raise ValueError('I/O operation on closed file.')
        self._files[self.name] = text + self.newline

    def writelines(self, lines: list):
        if self._closed:
            raise ValueError('I/O operation on closed file.')
        self._files[self.name] = self.newline.join(lines)

    def read(self):
        if self._closed:
            raise ValueError('I/O operation on closed file.')
        if self.name not in self._files:
            raise FileNotFoundError(f'No such file or directory: {self.name}')
        return self._files[self.name]

    def readlines(self):
        if self._closed:
            raise ValueError('I/O operation on closed file.')

        return self.read().split('\n')

    def readline(self):
        if self._closed:
            raise ValueError('I/O operation on closed file.')

        lines = self.readlines()
        if self.__read_line_no >= len(lines):
            return ''
        line = lines[self.__read_line_no]
        self.__read_line_no += 1
        return line

    def close(self):
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return f'<FileMock name={self.name} mode={self.mode} encoding={self.encoding} newline={self.newline}>'

    def __str__(self):
        return repr(self)


def run_tests(tests: List['TestCase'], environment: 'TrustedEnvironment'):
    for test in tests:
        test.run(environment)
