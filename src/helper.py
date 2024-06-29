import variables as v
import re

# returns true/false if TT+,A2s+ is valid syntax
def is_valid_expand(expand):
    return

def is_valid_hand(hand):
    if len(hand) == 2 and hand[0] == hand[1]:
        match = re.search(v.card_regex,hand[0])
        return bool(match)
    if len(hand) == 3 and hand[0] != hand[1]:
        match_1 = re.search('[SO]',hand[2])
        match_2 = re.search(str(v.card_regex + '{2}'),hand[0:2])
        return True if match_1 and match_2 else False
    return False


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
    return ret # return empty array if all else fails


# takes the hole cards and compares them to the part of the range in which the
# action was taken
def is_cards_in_range(cards,rang):
    return
