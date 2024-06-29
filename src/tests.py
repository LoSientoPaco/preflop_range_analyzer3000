import main as m
from helper import expand_card_syntax
import variables as v
import unittest


class TestHandAnalyser3000(unittest.TestCase):

    def test_expand1(self):
        self.assertEqual(expand_card_syntax('TT+'),['TT','JJ','QQ','KK','AA'])
        self.assertEqual(expand_card_syntax('22-99'),
                         ['22','33','44','55','66','77','88','99'])
        self.assertEqual(expand_card_syntax('22+'),
                         ['22','33','44','55','66','77','88','99','TT','JJ','QQ','KK','AA'])

    def test_expand2(self):
        self.assertEqual(expand_card_syntax('A2O+'),
                         ['A2O','A3O','A4O','A5O','A6O','A7O','A8O','A9O','ATO','AJO','AQO','AKO'])
        self.assertEqual(expand_card_syntax('K9S+'),['K9S','KTS','KJS','KQS'])
        self.assertEqual(expand_card_syntax('QJO+'),['QJO'])

    def test_expand3(self):
        self.assertEqual(expand_card_syntax('99-JJ'),['99','TT','JJ'])
        self.assertEqual(expand_card_syntax('92S-95S'),['92S','93S','94S','95S'])
        self.assertEqual(expand_card_syntax('T8O-T9O'),['T8O','T9O'])


    




if __name__ == "__main__":
    unittest.main()
