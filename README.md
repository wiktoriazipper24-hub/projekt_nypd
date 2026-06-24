# Literary Master Language Analyzer

A Python package for analyzing the language used in literary works and comparing them to a language dictionary.

## Installation

```bash
pip install git+https://github.com/wiktoriazipper24-hub/projekt_nypd.git
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
    main.py
    stats.py
    text_analysis.py
    data_processing.py
    similarity.py
tests/
raport.ipynb
```
