import json
from pathlib import Path
import logging as log
import Levenshtein
from itertools import product
from app.utils.tmp import comb1, comb2, comb3, comb4
from math import ceil


def open_config(fpath: str | Path) -> dict:
    fpath = Path(fpath)        
   
    with open(fpath, 'r', encoding="utf-8") as file:
        config = json.load(file)
    
    return config

def write_config(fpath: str | Path, config: dict):
    fpath = Path(fpath)        

    with open(fpath, 'w', encoding="utf-8") as file:
        json.dump(config, file)

def logger(*, name: str, fpath: Path | str):
    if not isinstance(fpath, Path):
        fpath = Path(fpath)

    if not fpath.exists():
        print(fpath.parents)

    try:
        abstract_logger = log.getLogger(name)
        abstract_logger.setLevel(log.DEBUG)

        abstract_logger_hand = log.FileHandler(filename=fpath, encoding='utf-8')
        abstract_logger_hand.setFormatter(log.Formatter('[%(asctime)s] %(levelname)s | %(message)s'))

        abstract_logger.addHandler(abstract_logger_hand)
    except Exception as exc:
        print(exc)
        raise
    else:
        return abstract_logger

def five_round(num):
    return ceil(num / 5) * 5

def std(word: str) -> str:
    if isinstance(word, str):
        return word.upper().replace('-', '').replace(' ', '').replace('.', '').replace('/', '').replace(',', '').strip()
    
def store_attribute(text: str):
    # Подготовка текста
    text = text.lower().strip()
    for el in "\\|/-;:":
        text.replace(el, '')

    word_list = text.split()[:4]
    twos_list = [iter_to_str(element) for element in delete_copyies(list(product(word_list, repeat=2)), 2)]
    thirds_list = [iter_to_str(element) for element in delete_copyies(list(product(word_list, repeat=3)), 3)]
    fourths_list = [iter_to_str(element) for element in delete_copyies(list(product(word_list, repeat=4)), 4)]
    print(word_list)

    # Поиск соответствий
    one_good_ids = check_ratio(word_list, comb1, 0.80)
    two_good_ids = check_ratio(twos_list, comb2, 0.75)
    three_good_ids = check_ratio(thirds_list, comb3, 0.70)
    four_good_ids = check_ratio(fourths_list, comb4, 0.65)

    temp_elements = [g[1] for g in sorted((one_good_ids, two_good_ids, three_good_ids, four_good_ids), key=lambda item: item[0], reverse=True)]
    print(temp_elements)
    all_elements = []
    for el in temp_elements:
        all_elements.extend(el)

    max_matches_count = 0
    max_matches = 82

    print(all_elements)
    for el in all_elements:
        if all_elements.count(el) > max_matches_count:
            max_matches_count = all_elements.count(el)
            max_matches = el
        
    return max_matches

        
def delete_copyies(lst, couple_count):
    death_note = []
    for i in range(len(lst)):
        if len(set(lst[i])) < couple_count:
            death_note.append(i)
        
    for enemy in sorted(death_note, reverse=True):
        del lst[enemy]
    
    return tuple(lst)

def iter_to_str(iterator):
    res = ""
    for e in iterator:
        res+=str(e)
        res+=' '
    return res.strip()


def check_ratio(names, pattern, good_percent):
    max_score = 0.0
    second_score = 0.0
    match = []
    for variant in names:
        # print(variant)
        for key_word in pattern:
            # print(key_word)
            ratio = Levenshtein.ratio(key_word, variant)

            if ratio >= good_percent:
                if max_score < ratio:
                    print(ratio, pattern[key_word])

                    match.insert(0, pattern[key_word])
                    max_score = ratio
                elif max_score >= ratio >= second_score:
                    print(ratio, pattern[key_word])
                    
                    match.insert(1, pattern[key_word])
                    second_score = ratio
                else:
                    match.append(pattern[key_word])
                    
    return max_score, match[:3]
