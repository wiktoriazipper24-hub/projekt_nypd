import sys
from unittest.mock import patch
from analyzer.main import main, build_arg_parser

def test_build_arg_parser():
    parser = build_arg_parser()
    args = parser.parse_args([
        "--dictionary", "odm.txt",
        "--works", "text1.txt,text2.txt",
        "--frequencies", "15",
        "--dictionary-stats",
        "--no-words",
        "--output", "test_wyniki.txt"
    ])
    assert args.dictionary == "odm.txt"
    assert args.works == "text1.txt,text2.txt"
    assert args.frequencies == 15
    assert args.no_words is True
    assert args.dictionary_stats is True
    assert args.output == "test_wyniki.txt"

def test_full_program_execution(tmp_path):
    dict_file = tmp_path / "odm.txt"
    dict_file.write_text("kot, koty\ndom, domy", encoding='utf-8')
    work_file = tmp_path / "work.txt"
    work_file.write_text("kot idzie do domu. dom stoi!", encoding='utf-8')
    work_file2 = tmp_path / "work2.txt"
    work_file2.write_text("pies biega po lesie.", encoding='utf-8')
    out_file = tmp_path / "out.txt"

    test_args = [
        "main.py", 
        "--dictionary", str(dict_file), 
        "--dictionary-stats",
        "--works", f"{str(work_file)},{str(work_file2)}",
        "--no-words", 
        "--frequencies", "2",
        "--output", str(out_file)
    ]
    
    with patch.object(sys, 'argv', test_args):
        main()

    assert out_file.exists()
    
    output_content = out_file.read_text(encoding='utf-8')
    assert "DICTIONARY STATISTICS" in output_content
    assert "WORKS STATISTICS" in output_content
    assert "MISSING WORDS" in output_content
    assert "TOTAL STATS FOR ALL WORKS" in output_content
    assert "FREQUENT WORDS" in output_content
    assert "Total words: 6" in output_content
    assert "kot" in output_content
