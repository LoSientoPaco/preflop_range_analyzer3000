### Author: Thomas Grutsch
import re
import variables as v
import helper as h
from jsonstream import load

# parses the config file
def grab_configs(config_file=None):
    configs = [] # array of dictionaries
    config = {}

    config_file = config_file if config_file else v.CONFIG
    
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '[Config]':
                continue
            if line == 'STOP':
                break
            match = re.search(r'^\d+:$',line)
            if match:
                config = {}
                continue
            if '=' in line:
                arr = line.split('=')
                config[arr[0]] = arr[1]
            if all(keys in config for keys in ('output_file','range_file','hand_files')):
                configs.append(config)
                config = {}
    
    return configs

# parses the range file
def parse_range_file(range_f):
    rang = {}
    with open(v.BASE_RANGES + range_f, 'r') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                arr = line.split(':')
                arr[0] = arr[0].strip()
                arr[1] = arr[1].strip().split(',')
                for i,ele in enumerate(arr[1]):
                    arr[1][i] = ele.strip().upper() # just upper everything for consistency
                rang[arr[0]] = arr[1]
    return rang
                
    
# parses the hand file and inserts the relevant infomation into a dictionary
def stream_hand_file(hand_f):
    f = open(v.BASE_HANDS + hand_f)
    return load(f)

# given hand_info and data['hands'], update the count
def add_hand_info_to_data(hand_info,hands):
    if hand_info['cards'] not in hands:
        hands[hand_info['cards']] = {hand_info['action']: 1}
        return hands
    if hand_info['actions'] not in hands[hand_info['cards']]:
        hands[hand_info['cards']] = {hand_info['action']: 1}
        return hands
    hands[hand_info['cards']][hand_info['action']] += hands[hand_info['cards']][hand_info['action']]
    return hands

# action in this case means the action found in rang for the hand
def print_analyze_hand(oput,hand,action,info):
   readable_hand = h.make_hand_readable(hand)
   total_played = h.get_total_played(info)
   oput.write(f'{readable_hand}:\n')
   oput.write(f'Inputted action: {action}, played {total_played} times in total.\n')
   for action,num in info.items():
       rang_action = h.map_action_codes(action)
       oput.write(f'Played {rang_action} {num} times. {round((num/total_played),2)*100}%\n')
       
   
   
   oput.write('\n')
   


def main():
    try:
        config = grab_configs()
        
        for c in config:
            sum = 0
            data = {'skipped_hands':0,'hands':{}}
            rang = parse_range_file(c['range_file'])
            hand_files = list(filter(None,c['hand_files'].split(',')))
            for hand_file in hand_files:
                hands = stream_hand_file(hand_file)
                for hand in hands:
                    if not h.is_valid_ohh(hand):
                        data['skipped_hands'] = data['skipped_hands'] + 1
                        continue
                    hand_info = h.parse_hand_json(hand)
                    if hand_info == {} or hand_info['action'] == "Invalid Action":
                        data['skipped_hands'] = data['skipped_hands'] + 1
                        continue
                    data['hands'] = add_hand_info_to_data(hand_info,data['hands'])
                    sum += 1
                
            # now have all hand info, time for data analysis
            print(rang)
            print(data)
            found_hands = []
            oput = open(v.BASE_OUTPUT + c['output_file'],'w')
            oput.write(f'Skipped Hands: {data["skipped_hands"]}\n')
            oput.write(f'Total Analyzed Hands: {sum - data["skipped_hands"]}\n\n')
            # loop thru each hand in the range, keeping track of each hand you process
            # then run through each hand that wasn't in range in data['hands']
            for action,hands in rang.items():
                oput.write(f'{action}:\n\n')
                for ele in hands:
                    for hand in h.expand_card_syntax(ele):
                        if hand in data['hands']:
                            found_hands.append(hand)
                            print_analyze_hand(oput,hand,action,data['hands'][hand])
                        else:
                            oput.write(f'{h.make_hand_readable(hand)} in {action} but never played.\n\n')

            oput.write('Hands found that were NOT in range:\n\n')
            for hand,info in data['hands'].items():
                if hand in found_hands:
                    continue
                print_analyze_hand(oput,hand,'Fold',info)
            oput.close()
                    
                    

                

    except Exception as e:
        print("Something Went Wrong!")
        print("Make sure files/configs/syntax is correct.")
        print(e)
    

if __name__ == "__main__":
    main()
