from Polynomial import Polynomial
import unittest

class TestPolynomial(unittest.TestCase):

    def setUp(self):
        self.w1 = Polynomial([1, 2, 3, 5])      # 1*x^3 + 2*x^2 + 3*x + 5
        self.w2 = Polynomial(5, 2, 1)           #         5*x^2 + 2*x + 1
        self.w3 = Polynomial(self.w1)

    def test_coefficients(self):
        self.assertEqual([5, 3, 2, 1], self.w1.coef_reverse)
        self.assertEqual([1, 2, 5], self.w2.coef_reverse)
        self.assertEqual([5, 3, 2, 1], self.w3.coef_reverse)
        c = self.w3.coef_reverse
        c.append(7)
        self.assertEqual([5, 3, 2, 1], self.w3.coef_reverse)

    def test_init(self):
        args = [1, 2, 3, 5]
        w = Polynomial(args)
        args.append(7)
        self.assertEqual([5, 3, 2, 1], w.coef_reverse)

    def test_str(self):
        self.assertEqual("x^3+2x^2+3x+5", str(self.w1))
        self.assertEqual("5x^2+2x+1", str(self.w2))

    def test_add(self):
        w3 = self.w2 + self.w1
        self.assertEqual([6, 5, 7, 1], w3.coef_reverse)
        w3 = self.w1 + self.w2
        self.assertEqual([6, 5, 7, 1], w3.coef_reverse)

    def test_sub(self):
        w3 = self.w2 - self.w1
        self.assertEqual([-4, -1, 3, -1], w3.coef_reverse)
        w4 = self.w1 - self.w2
        self.assertEqual([4, 1, -3, 1], w4.coef_reverse)


if __name__ == '__main__':
        unittest.main()
