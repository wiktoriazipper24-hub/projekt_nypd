from collections import Counter
from analyzer.stats import get_top_n_words, analyze_lines

def test_get_top_n_words():
    counter = Counter({'a': 10, 'b': 5, 'c': 5, 'd': 1})
    top_2 = get_top_n_words(counter, 2)
    expected = [('a', 10), ('b', 5), ('c', 5)]
    assert top_2 == expected

def test_get_top_n_words_empty():
    assert get_top_n_words(Counter(), 5) == []

def test_analyze_lines():
    lines = ["ala ma kota", "kot ma ale"]

    def dummy_extract(line):
        return line.split()

    stats = analyze_lines(lines, dummy_extract, count_chars_from_line=True)

    assert stats['lines'] == 2
    assert stats['total_words'] == 6
    assert stats['unique_words'] == 5
    assert ('ma', 2) in stats['top_words']
    
    def dummy_extract(line):
        return line.split()
        
    stats = analyze_lines(lines, dummy_extract, count_chars_from_line=True)
    
    assert stats['lines'] == 2
    assert stats['total_words'] == 6
    assert stats['unique_words'] == 5

def test_analyze_lines_skips_empty_words():
    lines = ["ala  kota"] 

    def dummy_extract_with_empty(line):
        return line.split(" ") 

    stats = analyze_lines(lines, dummy_extract_with_empty, count_chars_from_line=True)
    
    assert stats['total_words'] == 2
    assert stats['unique_words'] == 2