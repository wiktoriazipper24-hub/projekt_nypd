from analyzer.dictionary import load_dictionary
from analyzer.dictionary import get_dictionary_stats

def test_load_dictionary(tmp_path):
    dict_file = tmp_path / "odm.txt"
    dict_file.write_text("dom, domy, domem\nkot, koty, kotem", encoding='utf-8')
    words = load_dictionary(str(dict_file))
    expected = {'dom', 'domy', 'domem', 'kot', 'koty', 'kotem'}
    
    assert words == expected

def test_get_dictionary_stats(tmp_path):
    dict_file = tmp_path / "odm.txt"
    dict_file.write_text("kot, koty\ndom, domy", encoding='utf-8')
    stats = get_dictionary_stats(str(dict_file))

    assert stats['lines'] == 2
    assert stats['total_words'] == 4
    assert stats['unique_words'] == 4
    assert ('o', 4) in stats['letters'] or any(letter == 'o' for letter, _ in stats['letters'])
