import re
import urllib.request
from collections import Counter

DIACRITIC_PATTERN = re.compile(r'[āīūṅñṭḍṇśṣṃḥḷṙṚṝṜ]')

def load_english_words():
    url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
    with urllib.request.urlopen(url, timeout=10) as response:
        words = set(w.strip().upper() for w in response.read().decode('utf-8').splitlines())
    return words

ENGLISH_DICTIONARY = load_english_words()

def is_english(word):
    w = word.upper()
    if w in ENGLISH_DICTIONARY:
        return True
    if w.isdigit():
        return True
    if len(w) <= 2:
        return True
    return False

def is_non_english(word):
    if re.match(r'^[IVXLCDM]+[¦]*$', word):
        return False
    if DIACRITIC_PATTERN.search(word):
        return True
    if word[0].isupper() and len(word) > 1:
        if not is_english(word):
            return True
    return False

def process_file(filepath):
    non_english_words = Counter()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('<L>') or line.startswith('<LEND>'):
                continue
            
            if line.startswith('<'):
                continue
            
            line = re.sub(r'\{%.*?%\}', '', line)
            
            for word in line.split():
                word_clean = re.sub(r'[.,;:!?()"\']', '', word)
                if word_clean and is_non_english(word_clean):
                    non_english_words[word_clean] += 1
    
    return non_english_words.most_common()

def main():
    filepath = '/Users/dhaval/Documents/GithubRepos/sanskrit-lexicon/csl-orig/v02/pui/pui.txt'
    results = process_file(filepath)
    
    output_path = '/Users/dhaval/Documents/GithubRepos/other-sanskrit-lexicon-repos/PUI/issues/issue1/non_english_sorted.tsv'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("word\tcount\n")
        for word, count in results:
            f.write(f"{word}\t{count}\n")
    print(f"Output written to {output_path}")

if __name__ == '__main__':
    main()