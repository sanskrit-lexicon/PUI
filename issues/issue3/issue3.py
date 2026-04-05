import re
import urllib.request
from collections import Counter

def load_english_words():
    url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
    with urllib.request.urlopen(url, timeout=10) as response:
        return set(w.strip().upper() for w in response.read().decode('utf-8').splitlines())

ENGLISH_DICTIONARY = load_english_words()

def is_english(word):
    w = re.sub(r'[^a-zA-Z]', '', word).upper()
    if w in ENGLISH_DICTIONARY:
        return True
    if w.isdigit() or len(w) <= 2:
        return True
    return False

PATTERNS = [
    (r'[mn][kgṅcjñṭḍṇśṣsh]', '1_mn_kg'),
    (r'm[tdlv]', '2_m_tdlv'),
    (r'n[pbrl]', '3_n_pbrl'),
    (r'ṅ[^kgṅaāiīuūṛṝḷḹeo]', '4_ṅ_invalid'),
    (r'ñ[^cjñaāiīuūṛṝḷḹeo]', '5_ñ_invalid'),
    (r'ṇ[kgkgṅcjñtdnpbm]', '6_ṇ_invalid'),
]

def get_patterns(word):
    matches = []
    for pattern, label in PATTERNS:
        if re.search(pattern, word, re.IGNORECASE):
            matches.append(label)
    return matches

def main():
    filepath = '/Users/dhaval/Documents/GithubRepos/other-sanskrit-lexicon-repos/PUI/issues/issue1/pui_corrected.txt'
    
    improbable_words = Counter()
    
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
                word_clean = re.sub(r'<sup>\d+</sup>', '', word_clean)
                if word_clean and not is_english(word_clean):
                    patterns = get_patterns(word_clean)
                    if patterns:
                        improbable_words[word_clean] += 1
    
    results = improbable_words.most_common()
    
    output_path = '/Users/dhaval/Documents/GithubRepos/other-sanskrit-lexicon-repos/PUI/issues/issue3/improbable_words.tsv'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("word\tcount\tpattern\n")
        for word, count in results:
            patterns = get_patterns(word)
            for p in patterns:
                f.write(f"{word}\t{count}\t{p}\n")
    
    print(f"Found {len(results)} unique words matching improbable patterns")
    print(f"Output written to {output_path}")
    
    print("\nPattern counts:")
    pattern_counts = Counter()
    for word, count in results:
        for p in get_patterns(word):
            pattern_counts[p] += 1
    for p, c in sorted(pattern_counts.items()):
        print(f"  {p}: {c}")

if __name__ == '__main__':
    main()