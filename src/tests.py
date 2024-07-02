import main as m
from helper import expand_card_syntax,parse_hand_json
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


    def test_parse_hand_json1(self):
        pass

    def test_get_player_action1(self):
        # use the file test_hands_for_player_action.ohh
        # hand 1: folds to hero and goes all in => 0/All-in
        # 2: raises to hero and goes all in => 1/All-in
        # 3: 1/Raise, 4: 0/Raise 5: limps to hero: 0/Call 6: 0/Calls
        # 7: 0/Fold 8: 0/Raise 9: 1/Call 10: 1/Fold 11: Invalid
        config = m.grab_configs('../test_config.txt')[0]
        hands = m.stream_hand_file(config['hand_files'])
        self.assertEqual(parse_hand_json(next(hands))['action'],'0/All-in') #1
        self.assertEqual(parse_hand_json(next(hands))['action'],'1/All-in') #2
        self.assertEqual(parse_hand_json(next(hands))['action'],'1/Raise') #3
        self.assertEqual(parse_hand_json(next(hands))['action'],'0/Raise') #4
        self.assertEqual(parse_hand_json(next(hands))['action'],'0/Call')  #5
        self.assertEqual(parse_hand_json(next(hands))['action'],'0/Limp') #6
        self.assertEqual(parse_hand_json(next(hands))['action'],'0/Fold')
        self.assertEqual(parse_hand_json(next(hands))['action'],'0/Raise')
        self.assertEqual(parse_hand_json(next(hands))['action'],'1/Call')
        self.assertEqual(parse_hand_json(next(hands))['action'],'1/Fold')
        self.assertEqual(parse_hand_json(next(hands))['action'],'Invalid Action')



if __name__ == "__main__":
    unittest.main()
