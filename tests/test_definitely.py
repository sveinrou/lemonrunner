import unittest
from unittest.mock import MagicMock, call
from multiprocessing import Queue

from definitely import Definitely, DefinitelyRunnable

class RunnableTest(unittest.TestCase):
    def test_run_function(self):
        id = 'test'
        func = MagicMock()
        args = (1, 2)
        kwargs = {'foo': 'bar', 'a': 'b'}
        runnable = DefinitelyRunnable(id, target=func, args=args, kwargs=kwargs, times=3)
        runnable.run(MagicMock())
        func.assert_has_calls([call(*args, **kwargs)]*3)

class DefinitelyTest(unittest.TestCase):
    def test_timeout(self):
        pass

if __name__ == '__main__':
    unittest.main()
