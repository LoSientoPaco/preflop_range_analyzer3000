### Author: Thomas Grutsch
import re
import variables as v
import helper as h

# parses the config file
def grab_configs():
    configs = [] # array of dictionaries
    config = {}
    
    with open(v.CONFIG, 'r') as f:
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
def parse_hand_file(hand_f):
    return




# gets hand details and does logic to determine which part of the range to compare
# the hand with
def compare_hand_to_range(hand,rang):
    return


def main():
    config = grab_configs()

    for c in config:
        rang = parse_range_file(c['range_file'])
        print(rang)
    

if __name__ == "__main__":
    main()
