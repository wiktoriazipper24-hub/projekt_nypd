"""Core engine for computing word and letter frequency statistics."""

from collections import Counter

def analyze_lines(text_lines, extract_words_function, count_chars_from_line=False):
    """Analyzes a stream of lines and returns word/letter statistics.
    If count_chars_from_line=True, characters are counted from the raw line
    (used for works' files). Otherwise characters are counted only from
    extracted words (used for the dictionary)."""

    word_counter = Counter()
    letter_counter = Counter()
    total_words_count = 0
    line_count = 0

    for line in text_lines:
        line_count += 1

        if count_chars_from_line:
            letter_counter.update(line.replace('\n', ''))

        for word in extract_words_function(line):
            if not word:
                continue
            total_words_count += 1
            word_counter[word] += 1
            if not count_chars_from_line:
                letter_counter.update(word)

    return _compute_stats(word_counter, letter_counter, line_count, total_words_count)

def _compute_stats(word_counter, letter_counter, line_count, total_words_count):
    """Builds the final statistics report dict from raw word and letter counters."""
    unique_words_count = len(word_counter)
    top_words = get_top_n_words(word_counter, 10)
    letters_sorted, other_sorted = _split_and_sort_chars(letter_counter)

    return {
        "lines": line_count,
        "total_words": total_words_count,
        "unique_words": unique_words_count,
        "top_words": top_words,
        "letters": letters_sorted,
        "other_chars": other_sorted,
    }

def _split_and_sort_chars(letter_counter):
    """Splits character counts into letters and other characters, 
    both sorted by frequency then alphabetically."""
    letters_only = [(char, freq) for char, freq in letter_counter.items() if char.isalpha()]
    other_chars = [(char, freq) for char, freq in letter_counter.items() if not char.isalpha()]

    return (
        sorted(letters_only, key=_sort_by_frequency_then_alphabetically),
        sorted(other_chars, key=_sort_by_frequency_then_alphabetically),
    )

def _sort_by_frequency_then_alphabetically(item):
    return (-item[1], item[0])

def get_top_n_words(word_counter, n):
    """Returns top n words by frequency (with ties at the cutoff), 
    sorted by freq desc, then alphabetically."""

    sorted_all_words = sorted(word_counter.items(), key=lambda item: (-item[1], item[0]))

    if not sorted_all_words:
        return []

    cutoff_index = min(n, len(sorted_all_words)) - 1
    cutoff_freq = sorted_all_words[cutoff_index][1]
    return [(word, freq) for word, freq in sorted_all_words if freq >= cutoff_freq]
