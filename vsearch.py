def search_for_vowels(phrase: str) -> set:
    """Searching vowels in a inputing phrase"""
    vowels = set('aeiuo')
    return vowels.intersection(set(phrase))


def search_for_letters(phrase: str, letters: str='aeiou') -> set:
    """Searching custom letters in phrase, resolving them in set"""
    return set(letters).intersection(set(phrase))
