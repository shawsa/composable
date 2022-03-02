from composable import Composable
import unittest
# using sympy to test function equality
import sympy as sym
x = sym.symbols('x')

class TestComposable(unittest.TestCase):

    def test_compose(self):
        f = Composable(lambda x: x+1)
        g = lambda x: 2*x
        fog = f@g
        self.assertIsInstance(fog, Composable)
        self.assertEqual(fog(x).expand(), 2*x+1)

    def test_rcompose(self):
        f = lambda x: x+1
        g = Composable(lambda x: 2*x)
        fog = f@g
        self.assertIsInstance(fog, Composable)
        self.assertEqual(fog(x).expand(), 2*x+1)

    def test_multi_compose(self):
        f = Composable(lambda x: x*x)
        g = lambda x: 2*x
        h = lambda x: x + 1
        fogoh = f@g@h
        self.assertIsInstance(fogoh, Composable)
        self.assertEqual(fogoh(x).expand(), 4*x**2 + 8*x + 4)
        self.assertIsInstance(fogoh.function_tuple, tuple)
        for foo in fogoh.function_tuple:
            self.assertTrue(callable(foo))
        

    def test_pipe(self):
        f = Composable(lambda x: x+1)
        g = lambda x: 2*x
        fog = g | f
        self.assertIsInstance(fog, Composable)
        self.assertEqual(fog(x).expand(), 2*x+1)

    def test_rpipe(self):
        f = lambda x: x+1
        g = Composable(lambda x: 2*x)
        fog = g | f
        self.assertIsInstance(fog, Composable)
        self.assertEqual(fog(x).expand(), 2*x+1)

    def test_pipe_value(self):
        f = lambda x: x + 1
        g = lambda x: 2*x
        expr = x | (Composable() | g | f)
        self.assertEqual(expr, f(g(x)))

if __name__ == '__main__':
    unittest.main()
