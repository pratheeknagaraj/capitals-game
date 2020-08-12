#!/usr/bin/python3

import argparse
import colorama
import copy
import difflib
import os
import random
import string
import sys
import time
import unidecode

import capitals_augmented as capitals
import capitals_validate

colorama.init(autoreset=True)

class Color:
    GREEN = "\u001b[38;5;40m"
    RED = "\u001b[38;5;160m"

def get_capitals(args):
    data = capitals.data

    res = capitals_validate.validate(data)

    if not res:
        print("Failed to validate capitals")
        sys.exit(1)

    data_items = list(data.items())
    if not args.dependencies:
        data_items = [c for c in data_items if c[1].get('sovereign', True)]
    
    if args.regions or args.exclude_regions:
        new_data_items = []
        for data_item in data_items:
            select = (args.regions == None)
            for region in data_item[1]['regions']:
                if args.regions and region in args.regions:
                    select = True
                if args.exclude_regions and region in args.exclude_regions:
                    select = False
            if select:
                new_data_items.append(data_item)

        data_items = new_data_items

    if len(data_items) == 0:
        print(Color.RED + "Failed to select any capitals, use less restrictive region filters")
        sys.exit(1)

    return data_items

def shuffle_questions(arts, questions):
    qs = list(questions)
    if not args.alphabetize:
        random.shuffle(qs)
    return qs

def print_intro(data):
    print(colorama.Style.BRIGHT + "*** Welcome to the World Capitals Game ***")
    print()
    print(colorama.Fore.BLACK  + f"  Loaded {len(data)} capitals")
    print(colorama.Style.DIM    + "  Press CTL-C anytime to quit")
    print()

def print_results(args, info):
    correct_count = len(info.correct)
    wrong_count = len(info.wrong)
    accuracy = 0 if info.total == 0 else correct_count * 100 / float(info.total)
    avg_time = 0 if info.total == 0 else info.total_time / float(info.total)

    print()
    print()
    print("Results:")
    print(colorama.Style.BRIGHT +                        f"  Total    : {info.total}")
    print(colorama.Style.BRIGHT + colorama.Fore.GREEN  + f"  Correct  : {correct_count}")
    print(colorama.Style.BRIGHT + colorama.Fore.RED    + f"  Wrong    : {wrong_count}")
    print(colorama.Style.BRIGHT + colorama.Fore.YELLOW + f"  Accuracy : {accuracy:.2f}%")
    print()
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN   + f"  Total Response Time   : {info.total_time:6.1f} secs")
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN   + f"  Average Response Time : {avg_time:6.3f} secs")

    if args.full_results:
        if correct_count > 0:
            print()
            print("  Correct Table")
            for elem in info.record:
                num, res, question = elem
                if res[0] == True:
                    country = question[0]
                    capital_str = res[2]
                    print(Color.GREEN + f"    {num:3d}. {country:35s} - {capital_str:<s}")
        
        if wrong_count > 0:
            print()
            print("  Wrong Table")
            for elem in info.record:
                num, res, question = elem
                if res[0] == False:
                    country = question[0]
                    capital_str = res[2]
                    print(Color.RED + f"    {num:3d}. {country:35s} - {capital_str:<s}")

class GameInfo:

    def __init__(self):
        self.correct = []
        self.wrong = []
        self.total = 0

        self.total_time = 0

        self.record = []

    def update(self, num, res, question):
        self.record.append((num, res, question))

        is_right = res[0]
        if is_right:
            self.correct.append(question)
        else:
            self.wrong.append(question)
        self.total = num
        self.total_time += res[3]

def ask(args, num, question):
    country = question[0]
    capital_info = question[1]

    question_str = "What is the capital of"
    if len(capital_info['capital']) > 1:
        question_str = "What is _a_ capital of"

    start_time = time.time()
    answer = input(colorama.Style.RESET_ALL + f"{num:3d}. {question_str} " + colorama.Style.BRIGHT + country + colorama.Style.RESET_ALL + "? " + colorama.Fore.YELLOW)
    stop_time = time.time()
    
    total_time = stop_time - start_time

    res = check(args, answer, capital_info, total_time)
    return res

table = str.maketrans(dict.fromkeys(string.punctuation))

def clean(s):
    return unidecode.unidecode(s.translate(table)).lower()

def forgive(s):
    # Allow for some common forgiving omissions or replacements
    return s.replace(' city', '').replace('saint', 'st')

def similar(a, b):
    # 85% similarity index is a heuristic based on some simple testing
    return (difflib.SequenceMatcher(None, a, b).ratio() > 0.85)

def check(args, answer, capital_info, total_time):

    time_str = ""
    if args.timing:
        time_str = colorama.Fore.WHITE + colorama.Style.DIM + f"[{total_time:5.1f}s] " + colorama.Style.RESET_ALL

    ans_clean = clean(answer.strip())
   
    valid = capital_info['capital']
   
    multi = False
    if len(valid) > 1:
        capitals_str = ", ".join(list(valid))
        correct_str = "The capitals are: " + colorama.Style.BRIGHT + capitals_str
        multi = True
    else:
        capitals_str = list(valid)[0]
        if type(capitals_str) == tuple:
            capitals_str = '/'.join(capitals_str)
        correct_str = "The capital is: " + colorama.Style.BRIGHT + capitals_str

    def check_conditions(e, ans_clean, multi, capitals_str):

        extra_feedback = ""
        correct = False

        if clean(e) == ans_clean:
            correct = True
        elif forgive(clean(e)) == forgive(ans_clean):
            extra_feedback = colorama.Fore.BLUE + " More precisely: " + colorama.Style.BRIGHT + capitals_str
            correct = True

        if not correct:
            if not args.spelling and similar(forgive(clean(e)), forgive(ans_clean)):
                extra_feedback = colorama.Fore.MAGENTA + " Check your spelling: " + colorama.Style.BRIGHT + capitals_str
                correct = True

        if not extra_feedback and correct and multi:
            extra_feedback = colorama.Fore.CYAN + " More completely: " + colorama.Style.BRIGHT + capitals_str
        
        if correct:
            print("    " + time_str + Color.GREEN + "Correct!" + extra_feedback)
            return True
        
        return False

    for elem in valid:

        # Tuples are used for alternative spellings of same capital city
        if type(elem) != tuple:
            elem = [elem]

        for e in elem:
            r = check_conditions(e, ans_clean, multi, capitals_str)
            if r:
                return True, answer, capitals_str, total_time

    print("    " + time_str + Color.RED + "Incorrect. " + correct_str)
    return False, answer, capitals_str, total_time
    
def run_game(args, info, questions):
    num = 1
    while True:
        available_questions = copy.deepcopy(questions)
        available_questions = shuffle_questions(args, available_questions)
        for question in available_questions:
            res = ask(args, num, question)
            info.update(num, res, question) 
            time.sleep(0.25)
            num += 1
        if not args.infinite:
            break

def run(args, data):
    try:
        print_intro(data)
        info = GameInfo()
        run_game(args, info, data)
    except KeyboardInterrupt:
        pass
    
    print_results(args, info)

def main(args):
    data = get_capitals(args)
    run(args, data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='World Capitals Game', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-a', '--alphabetize', action='store_true', help='Alphabetize Countries')
    parser.add_argument('-d', '--dependencies', action='store_true', help='Include Dependencies')
    parser.add_argument('-e', '--exclude-regions', type=str, nargs='+', default=None, choices=capitals_validate.ALLOWED_REGIONS, help='Exclude selected regions')
    parser.add_argument('-f', '--full-results', action='store_true', help='Show Full Results')
    parser.add_argument('-i', '--infinite', action='store_true', help='Infinite mode, cycle indefinitely')
    parser.add_argument('-r', '--regions', type=str, nargs='+', default=None, choices=capitals_validate.ALLOWED_REGIONS, help='Show Only Countries from selected regions')
    parser.add_argument('-s', '--spelling', action='store_true', help='Require correct spellings')
    parser.add_argument('-t', '--timing', action='store_true', help='Show Timing per Question')
    
    args = parser.parse_args()

    main(args)

