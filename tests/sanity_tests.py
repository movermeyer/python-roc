import unittest
from test_data.pow_fixture import PowFixture


class PowFixtureTestCase(unittest.TestCase):
    def test_3_in_power_of_2_is_9(self):
        self.assertEqual(PowFixture(3).pow(2), 9)


if __name__ == '__main__':
    unittest.main()
