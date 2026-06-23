# Literary Master Language Analyzer

A Python package for analyzing the language used in literary works and comparing them to a language dictionary.

## Installation

```bash
pip install .
```

## Usage

```bash
py -m analyzer.main --dictionary odm.txt --works text1.txt,text2.txt --dictionary-stats --no-words --frequencies 15 --output results.txt
```

## Arguments

- `--dictionary` — path to the dictionary file
- `--works` — comma-separated list of work files to analyze
- `--dictionary-stats` — display statistics for the dictionary and works
- `--no-words` — show words from works that are missing from the dictionary
- `--frequencies N` — show N most frequent words per file
- `--output` — path to the output file (required)

## Running tests

```bash
py -m pytest tests/ --cov=analyzer
```

## Project structure

```
analyzer/
    main.py           - command-line entry point
    stats.py          - core statistics engine
    text_analysis.py  - text cleaning and word extraction
    data_processing.py - dictionary loading and statistics
    similarity.py     - cosine similarity style comparison
tests/
    test_*.py         - unit and integration tests
raport.ipynb          - Jupyter notebook with statistics and charts
```