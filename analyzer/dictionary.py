"""Functions for loading and analyzing the language dictionary file."""

from analyzer.stats import analyze_lines

def load_dictionary(file_path):
    """Reads a dictionary file and returns the set of all valid word forms."""
    valid_words = set()
    for line in _yield_dictionary_lines(file_path):
        for form in _extract_dictionary_forms(line):
            valid_words.add(form)
    return valid_words

def _yield_dictionary_lines(file_path):
    """Yields non-empty lines from a dictionary file, one at a time."""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                yield line

def _extract_dictionary_forms(line):
    """Splits one dictionary line into a list of words, skipping empty ones."""
    return [form for form in line.strip().split(", ") if form]

def get_dictionary_stats(file_path):
    """Computes word and letter frequency statistics for the dictionary file."""
    return analyze_lines(
        _yield_dictionary_lines(file_path),
        _extract_dictionary_forms,
        count_chars_from_line=False,
    )
