import sys, random, math, re
from collections import Counter

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

EN_FREQ_ORDER = "etaoinshrdlcumwfgypbvkjxqz"
COMMON_WORDS = {
    "the","be","to","of","and","a","in","that","have","i","it","for","not","on",
    "with","he","as","you","do","at","this","but","his","by","from","they","we",
    "say","her","she","or","an","will","my","one","all","would","there","their",
    "what","so","up","out","if","about","who","get","which","go","me","when",
    "make","can","like","time","no","just","him","know","take","people","into",
    "year","your","good","some","could","them","see","other","than","then","now",
    "look","only","come","its","over","think","also","back","after","use","two",
    "how","our","work","first","well","way","even","new","want","because","any",
    "these","give","day","most","us"
}
LETTERS = "abcdefghijklmnopqrstuvwxyz"

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def apply_mapping(ciphertext, mapping):
    out = []
    for ch in ciphertext:
        if ch.isalpha():
            lower = ch.lower()
            mapped = mapping.get(lower, lower)
            out.append(mapped.upper() if ch.isupper() else mapped)
        else:
            out.append(ch)
    return "".join(out)

def make_initial_mapping(ciphertext):
    cnt = Counter([c for c in ciphertext.lower() if c.isalpha()])
    freq_sorted = [p for p,_ in cnt.most_common()]
    mapping = {}
    used = set()
    for i,c in enumerate(freq_sorted):
        if i < len(EN_FREQ_ORDER):
            mapping[c] = EN_FREQ_ORDER[i]
            used.add(EN_FREQ_ORDER[i])
    leftover = [ch for ch in LETTERS if ch not in used]
    for ch in LETTERS:
        if ch not in mapping:
            mapping[ch] = leftover.pop(0) if leftover else random.choice(LETTERS)
    return mapping

def word_based_score(plaintext):
    words = re.findall(r"[a-z']+", plaintext.lower())
    if not words:
        return -1000.0
    score = 0.0
    for w in words:
        if w in COMMON_WORDS:
            score += 3.0 + 0.3 * len(w)
        score += 0.01 * len(w)
        if len(w) == 1 and w not in ('a','i'):
            score -= 0.8
    score -= 0.001 * sum(plaintext.lower().count(ch*3) for ch in LETTERS)
    return score

def letter_freq_score(plaintext):
    cnt = Counter([c for c in plaintext.lower() if c.isalpha()])
    total = sum(cnt.values()) or 1
    english_freq = {
        'e': 12.0, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
        's': 6.3, 'r': 6.0, 'h': 6.1, 'l': 4.0, 'd': 4.3, 'c': 2.8,
        'u': 2.8, 'm': 2.4, 'f': 2.2, 'y': 2.0, 'w': 2.4, 'g': 2.0,
        'p': 1.9, 'b': 1.5, 'v': 1.0, 'k': 0.8, 'x': 0.15, 'q': 0.1, 'j': 0.15, 'z': 0.07
    }
    sc = 0.0
    for ch,ef in english_freq.items():
        observed = 100.0 * cnt.get(ch,0)/total
        sc -= abs(observed - ef) * 0.02
    return sc

def fitness(plaintext):
    return 1.0 * word_based_score(plaintext) + 0.6 * letter_freq_score(plaintext)

def solve(ciphertext, restarts=20, iters_per_restart=8000):
    base_map = make_initial_mapping(ciphertext)
    best_overall = None
    best_score = -1e9
    for restart in range(restarts):
        if restart == 0:
            mapping = base_map.copy()
        else:
            perm = list(LETTERS)
            random.shuffle(perm)
            mapping = {c: p for c,p in zip(LETTERS, perm)}
        current_plain = apply_mapping(ciphertext, mapping)
        current_score = fitness(current_plain)
        T = 1.0 + 0.5 * (restarts - restart)
        for i in range(iters_per_restart):
            a,b = random.sample(LETTERS, 2)
            m2 = mapping.copy()
            m2[a], m2[b] = m2[b], m2[a]
            pt2 = apply_mapping(ciphertext, m2)
            s2 = fitness(pt2)
            delta = s2 - current_score
            if delta > 0 or random.random() < math.exp(delta / max(T, 1e-9)):
                mapping = m2
                current_score = s2
                current_plain = pt2
                if current_score > best_score:
                    best_score = current_score
                    best_overall = (mapping.copy(), current_plain, best_score)
            T *= 0.99995
    return best_overall

def print_mapping(mapping):
    pairs = sorted(mapping.items())
    for c,p in pairs:
        sys.stdout.write(f"{c}->{p}; ")
    sys.stdout.write("\n")

def main():
    if len(sys.argv) >= 2:
        text = load_text(sys.argv[1])
    else:
        print("Paste ciphertext then EOF:")
        text = sys.stdin.read()
    text = text.strip()
    if not text:
        print("No input.")
        return
    print("Solving...")
    mapping, plaintext, score = solve(text)
    print("\n=== Best plaintext (score={:.2f}) ===\n".format(score))
    print(plaintext)
    print("\n=== Mapping ===")
    print_mapping(mapping)

if __name__ == "__main__":
    main()
