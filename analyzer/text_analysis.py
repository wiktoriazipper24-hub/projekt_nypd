"""Functions for analyzing the Master's literary works: cleaning text,
extracting words, computing statistics, and finding words missing from
the dictionary."""

from collections import Counter
from analyzer.stats import analyze_lines

punctuation_to_remove = set(""".,;:"“”"„\\/'‘’!?()[]}{-_—«»*•™$%+0123456789#""")

def clean_and_extract_words(line):
    """Removes punctuation and digits from a line and splits it into a list of words."""
    cleaned_chars = []
    for char in line:
        if char in punctuation_to_remove:
            cleaned_chars.append(' ')
        else:
            cleaned_chars.append(char)
    cleaned_line = ''.join(cleaned_chars)
    return cleaned_line.split()

def _yield_lines_from_files(file_paths):
    """Yields lines from one file or multiple files, one at a time."""
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            yield from file


def get_works_stats(file_paths):
    """Computes word and letter frequency statistics for one or multiple files."""
    return analyze_lines(
        _yield_lines_from_files(file_paths),
        clean_and_extract_words,
        count_chars_from_line=True,
    )


def find_missing_words(file_paths, dictionary_words):
    """Finds words used in the given file(s) that do not exist in the dictionary
    (case-insensitive), and returns them sorted by frequency, then alphabetically."""
    dictionary_lower = {word.lower() for word in dictionary_words}
    missing_counter = Counter()

    for line in _yield_lines_from_files(file_paths):
        for word in clean_and_extract_words(line):
            if word.lower() not in dictionary_lower:
                missing_counter[word] += 1

    return sorted(missing_counter.items(), key=lambda item: (-item[1], item[0]))

def get_word_counter_for_file(file_path):
    """Returns a Counter of word frequencies for a single file 
    (needed for --frequencies and style comparison)."""
    word_counter = Counter()
    for line in _yield_lines_from_files(file_path):
        for word in clean_and_extract_words(line):
            word_counter[word] += 1
    return word_counter
