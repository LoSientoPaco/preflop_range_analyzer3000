### File Paths
BASE_HANDS="../hands/"
BASE_RANGES="../ranges/"
BASE_OUTPUT="../outputs/"
CONFIG="../config.txt"
###


### Poker Variables
reverse_rank = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
rank = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
TOP_RANK = 13
suites = ['s','h','c','d']
positions = ['UTG','UTG2','UTG3','LJ','HJ','CO','BTN','SB','BB']
card_regex = '[2-9TJQKA]'
actions = ['Fold','Limp','Call','Raise','3-Bet','All-in','Call/Limp']

### OHH Variables
get_hero = ['ohh','hero_player_id']
preflop_action = ['ohh','rounds',0,'action']


### Example Datas
hand_info = {'cards':"A2S",
             'action':"All-in",
             'in-range': True}
