import variables as v
import re

# returns true/false if TT+,A2s+ is valid syntax
def is_valid_expand(expand):
    return

# returns T/F if hand is valid or not
def is_valid_hand(hand):
    if len(hand) == 2 and hand[0] == hand[1]:
        match = re.search(v.card_regex,hand[0])
        return bool(match)
    if len(hand) == 3 and hand[0] != hand[1]:
        match_1 = re.search('[SO]',hand[2])
        match_2 = re.search(str(v.card_regex + '{2}'),hand[0:2])
        return True if match_1 and match_2 else False
    return False

# gets the index of the rank of the card in v.rank
def get_rank_index(card_rank):
    for i,ele in enumerate(v.rank):
        if card_rank == ele:
            return i

# takes TT+ or A2o+ and return an array of hands
def expand_card_syntax(expand):
    ret = []
    if '+' in expand:
        if len(expand) == 3 and expand[0] == expand[1]: # we have pairs
            index = get_rank_index(expand[0])
            for i in range(index,v.TOP_RANK):
                ret.append(str(v.rank[i] + v.rank[i]))
            return ret
        if len(expand) == 4: # everything else
            index = get_rank_index(expand[1])
            l_index = get_rank_index(expand[0])
            for i in range(index,l_index):
                ret.append(str(expand[0] + v.rank[i] + expand[2]))
            return ret
    if '-' in expand:
        if len(expand) == 5 and expand[0] == expand[1]: # we have pairs
            f_index = get_rank_index(expand[0])
            l_index = get_rank_index(expand[3]) + 1 # how range(i,y) works
            for i in range(f_index,l_index):
                ret.append(str(v.rank[i] + v.rank[i]))
            return ret
        if len(expand) == 7: # everything else
            f_index = get_rank_index(expand[1])
            l_index = get_rank_index(expand[5]) + 1
            for i in range(f_index,l_index):
                ret.append(str(expand[0] + v.rank[i] + expand[2]))
            return ret
    return [expand] # return the hand in an array

# sets the higher rank card first in the hand.
def have_higher_rank_first(cards):
    first = get_rank_index(cards[0])
    second = get_rank_index(cards[1])
    if first >= second:
        return cards
    else:
        return str(cards[1] + cards[0] + cards[2])
    
    

# takes the hole cards and compares them to the part of the range in which the
# action was taken
def is_cards_in_range(cards,rang):
    return

# returns T/F if the hand is valid for this program. 
def is_valid_ohh(hand):
    try:
        hand = hand['ohh']
        if 'hero_player_id' not in hand:
            return False
        if 'rounds' not in hand:
            return False
        if hand['rounds'][0]['street'] != 'Preflop':
            return False
    except Exception as e:
        return False
    return True

# get the player action from list of preflop actions
def get_player_action(actions,hero_id,bb_amt):
    others = [] # others actions
    for action in actions:
        if 'Post' in action['action']:
            continue
        if action['action'] == 'Dealt Cards':
            continue
        if action['action'] == 'Fold' and action['player_id'] != hero_id:
            continue
        if action['player_id'] != hero_id:
            others.append(action['action'])
        if action['player_id'] == hero_id:
            if len(others) == 0: # folded to hero
                if action['action'] == 'Fold':
                  return '0/Fold'
                if action['action'] == 'Call':
                    return '0/Limp'
                if action['amount'] > bb_amt:
                    if action['is_allin']:
                        return '0/All-in'
                    return '0/Raise'
            if len(others) > 0 and others.count('Raise') == 0:
                if action['action'] == 'Fold':
                    return '0/Fold'
                if action['action'] == 'Call':
                    return '0/Call'
                if action['action'] == 'Raise':
                    if action['is_allin']:
                        return '0/All-in'
                    return '0/Raise'
            if others.count('Raise') == 1:
                if action['action'] == 'Fold':
                    return '1/Fold'
                if action['action'] == 'Call':
                    return '1/Call'
                if action['action'] == 'Raise':
                    if action['is_allin']:
                        return '1/All-in'
                    return '1/Raise'
            if others.count('Raise') > 1:
                return "Invalid Action" # future update for 3-bet / 4-bets?
    return "Invalid Action"
    
# parses hand data and returns the relevant information
def parse_hand_json(hand):
    try:
        hand = hand['ohh']
        hand_info = {}
        hero_id = hand['hero_player_id']
        for action in hand['rounds'][0]['actions']:
            if action['action'] == 'Dealt Cards' and action['player_id'] == hero_id:
                cards = action['cards'][0] + action['cards'][1]
                if cards[0] == cards[2]:
                    cards = cards[0] + cards[2]
                elif cards[1] == cards[3]:
                    cards = cards[0] + cards[2] + 'S'
                else:
                    cards = cards[0] + cards[2] + 'O'
                hand_info['cards'] = have_higher_rank_first(cards)
        hand_info['action'] = get_player_action(hand['rounds'][0]['actions'],
                                                hero_id,hand["big_blind_amount"])
        return hand_info
    except Exception as e:
        print("Unable to parse Hand.")
        print(e)
        print('********')
        return {}

# K3O > K3o
def make_hand_readable(hand):
    if len(hand) == 2:
        return hand
    return hand[0:2] + hand[2].lower()

# determine where in range if cant be found return fold, not needed currently
def where_in_range(hand,rang):
    for action,hands in rang.items():
        for ele in hands:
            if hand in expand_card_syntax(ele):
                return action
    return 'Fold'
        
def get_total_played(info):
    sum = 0
    for action,num in info.items():
        sum += num
    return num

# 0/All-In > All-In, 1/All-in > 3Bet-All-In
def map_action_codes(action):
    match action:
        case '0/Raise':
            return 'Raise'
        case '0/Limp':
            return 'Limp'
        case '0/Fold':
            return 'Fold'
        case '0/Call':
            return 'Limped Behind'
        case '0/All-In':
            return 'All-In'
        case '1/Raise':
            return '3Bet'
        case '1/Call':
            return 'Call'
        case '1/Fold':
            return 'Fold'
        case '1/All-in':
            return '3Bet-All-In'
    return ""
