# Group all words into 1 common dict
def word_grouper(word_dicts):
    from collections import Counter

    c = Counter()
    for word_dict in word_dicts:
        c.update(word_dict)
    return c
