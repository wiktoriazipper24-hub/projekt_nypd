from analyzer.text_analysis import clean_and_extract_words, find_missing_words, get_works_stats

def test_clean_and_extract_words():
    line = "Ona powiedziała: „Witaj 123”."
    expected = ['Ona', 'powiedziała', 'Witaj']
    assert clean_and_extract_words(line) == expected

def test_find_missing_words(tmp_path):
    test_file = tmp_path / "test_work.txt"
    test_file.write_text("Ala ma kota i psa", encoding='utf-8')
    dictionary_words = {'ala', 'ma', 'psa'}
    missing = find_missing_words([str(test_file)], dictionary_words)
    expected = [('i', 1), ('kota', 1)]
    assert missing == expected

def test_get_works_stats_single_file(tmp_path):
    file1 = tmp_path / "work1.txt"
    file1.write_text("ala ma kota", encoding='utf-8')

    stats = get_works_stats(str(file1))

    assert stats['lines'] == 1
    assert stats['total_words'] == 3


def test_get_works_stats_multiple_files(tmp_path):
    file1 = tmp_path / "work1.txt"
    file1.write_text("ala ma kota", encoding='utf-8')

    file2 = tmp_path / "work2.txt"
    file2.write_text("kot ma ale", encoding='utf-8')

    stats = get_works_stats([str(file1), str(file2)])

    assert stats['lines'] == 2
    assert stats['total_words'] == 6