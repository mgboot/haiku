import random
import string

def get_pron_dict():
    """ returns pronunciation dictionary (from The CMU Pronouncing Dictionary) with words as keys and phoneme codes as values """
    p = open("pronunciation_dict.txt", encoding='utf8').read()
    lines = p.split('\n')
    prons = dict()
    for line in lines:
        prons[line.split()[0]] = line.split()[1:]
    return prons

def get_lexicon(path):
    """ returns a dictionary (with words as keys and counts as values) for the txt file at path. """
    s = open(path, encoding='utf8').read()
    s_tokens = s.split()
    lexicon = dict()
    for token in s_tokens:
        # Pronouncing Dictionary uses all uppercase, so lexicon will too:
        t = token.upper().strip(string.punctuation + "‘’")
        lexicon[t] = lexicon.get(t, 0) + 1 # create OR increment lexicon entry for token
    return lexicon

def filter_dict(pron_dict, lexicon):
    """ deletes keys in the Pronouncing Dictionary that do not occur in lexicon. """
    for k in list(pron_dict.keys()):
        if k not in lexicon:
            del pron_dict[k]
    return None

def print_dict(d):
    """ print dictionary with one entry per line """
    for key in d:
        print(key, ':\t', d[key])
    return None

def get_syl_count_dict(pron_dict):
    """ takes a pronunciation dictionary and returns a dictionary with the same keys but values are syllable count for each word."""
    """ We're working with haikus which deal exclusively with syllable counts and so
    do not need to worrk about word-stress patterns as we would for other types of poetry. """
    syl_counts = dict()
    for key in pron_dict:
        phonemes = pron_dict[key]
        syls = 0
        """ in The Pronouncing Dictionary format, all vowels (and no consonants) end with a numeral from 0 to 2
        (to indicate their position in the stress hierarchy;
        so, to count the number of syllables in a word we need only count the vowels. """
        for ph in phonemes:
            if ph[-1] >= '0' and ph[-1] <= '2':
                syls += 1
        syl_counts[key] = syls
    return syl_counts

def count_syls(syl_counts, words):
    """ given a list of words that occur in the syllable counts dictionary, return the sum of syllable counts. """
    sum = 0
    for w in words:
        sum += syl_counts[w.upper()]
    return sum

def random_line(syl_counts, syls):
    """ returns a string of random words from the syllable count dictionary, given a specified number of syllables. """
    words = []
    while count_syls(syl_counts, words) < syls:
        new_word = random.choice(list(syl_counts.keys()))
        if new_word not in words:
            words.append(new_word)
        if count_syls(syl_counts, words) > syls:
            del words[-1]
    for i in range(len(words)):
        words[i] = words[i].lower()
    words[0] = words[0].capitalize()
    return ' '.join(words)

def print_haiku(syl_counts):
    haiku = []
    haiku.append(random_line(syl_counts, 5))
    haiku.append(random_line(syl_counts, 7))
    haiku.append(random_line(syl_counts, 5))
    for line in haiku:
        print(line)
    print()
    return None

if __name__ == "__main__":

    d = get_pron_dict()
    filter_dict(d, get_lexicon("silmarillion.txt"))

    s = get_syl_count_dict(d)
    
    for _ in range(100):
        print_haiku(s)
