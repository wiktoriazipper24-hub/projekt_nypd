"""Command-line entry point for the Literary Master Language Analyzer."""

import argparse
from analyzer.data_processing import load_dictionary, get_dictionary_stats
from analyzer.text_analysis import get_works_stats, find_missing_words
from analyzer.stats import get_top_n_words
from analyzer.text_analysis import get_word_counter_for_file


def print_word_stats(stats, out, top_label="Top words with most occurrences (including ties):"):
    """Prints word, letter and character frequency statistics to the given output stream."""
    print(f"Total lines: {stats['lines']}", file=out)
    print(f"Total words: {stats['total_words']}", file=out)
    print(f"Unique words: {stats['unique_words']}", file=out)

    print(f"\n{top_label}", file=out)
    for word, freq in stats['top_words']:
        print(f"  - {word}: {freq} times", file=out)

    print("\nCharacter frequencies (sorted by occurrence):", file=out)
    for char, freq in stats['letters']:
        print(f"  '{char}': {freq}", file=out)

    print("\nOther character frequencies (sorted by occurrence):", file=out)
    for char, freq in stats['other_chars']:
        char_display = f"'{char}'" if char.strip() else f"space ({repr(char)})"
        print(f"  {char_display}: {freq}", file=out)


def handle_dictionary(args, out):
    """Loads the dictionary file and optionally prints its statistics to the output stream.
    Returns the set of valid word forms for use in missing words analysis."""
    print(f"Loading dictionary from: {args.dictionary}...", file=out)
    dictionary_words = load_dictionary(args.dictionary)
    print(f"Success! Loaded {len(dictionary_words)} unique word forms.", file=out)

    if args.dictionary_stats:
        print("\n=== DICTIONARY STATISTICS ===", file=out)
        print_word_stats(get_dictionary_stats(args.dictionary), out)

    return dictionary_words


def handle_works_stats(works_files, out):
    """Prints per-file statistics for each work,
    and combined statistics if more than one file is given."""
    print("\n=== WORKS STATISTICS ===", file=out)

    for file_path in works_files:
        print(f"\n--- Stats for file: {file_path} ---", file=out)
        try:
            # Here we pass a single string (one file)
            print_word_stats(get_works_stats(file_path), out, "Top 10 most frequent words:")
        except FileNotFoundError:
            print(f"Error: Could not find file {file_path}", file=out)

    if len(works_files) > 1:
        print("\n=== TOTAL STATS FOR ALL WORKS ===", file=out)
        # Here we pass the exact same function a list of files!
        total_stats = get_works_stats(works_files)
        print(f"Total files analyzed: {len(works_files)}", file=out)
        print_word_stats(total_stats, out, "Top 10 most frequent words overall:")


def handle_missing_words(works_files, dictionary_words, out):
    """Finds and prints words from the works that are missing from the dictionary."""
    if not dictionary_words:
        print("\nError: You must provide a valid --dictionary to analyze missing words.", file=out)
        return

    print("\n=== MISSING WORDS ANALYSIS ===", file=out)
    missing_words = find_missing_words(works_files, dictionary_words)

    if not missing_words:
        print("All words from the works exist in the dictionary!", file=out)
        return

    total_missing_occurrences = sum(freq for _, freq in missing_words)
    print(f"Total unique missing words: {len(missing_words)}", file=out)
    print(f"Total occurrences of missing words: {total_missing_occurrences}", file=out)
    print("\nList of missing words (sorted by frequency, then alphabetically):", file=out)
    for word, freq in missing_words[:1000]:
        print(f"  - {word}: {freq} times", file=out)


def handle_frequencies(works_files, n, out):
    """Prints the n most frequent words for each work file."""
    print(f"\n=== TOP {n} FREQUENT WORDS PER FILE ===", file=out)
    for file_path in works_files:
        print(f"\n--- {file_path} ---", file=out)
        counter = get_word_counter_for_file(file_path)
        top_words = get_top_n_words(counter, n)
        for word, freq in top_words:
            print(f"  - {word}: {freq} times", file=out)


def build_arg_parser():
    """Builds and returns the command-line argument parser."""
    parser = argparse.ArgumentParser(description="Literary Master Language Analyzer")
    parser.add_argument("--dictionary", type=str,
                        help="Path to the dictionary file")
    parser.add_argument("--dictionary-stats", action="store_true",
                        help="Display dictionary and works stats")
    parser.add_argument("--works", type=str,
                        help="Comma-separated list of Master's works")
    parser.add_argument("--no-words", action="store_true",
                        help="Analyze words that are not in dictionary")
    parser.add_argument("--frequencies", type=int, metavar="N",
                        help="Gives N most frequent words")
    parser.add_argument("--output", type=str, required=True,
                        help="Path to output file for results")
    return parser


def main():
    """Parses command-line arguments and runs the requested analyses, 
    writing results to the output file."""
    args = build_arg_parser().parse_args()

    with open(args.output, 'w', encoding='utf-8') as out:
        dictionary_words = set()
        if args.dictionary:
            dictionary_words = handle_dictionary(args, out)

        if args.works:
            works_files = [f.strip() for f in args.works.split(',')]

            if args.dictionary_stats:
                handle_works_stats(works_files, out)

            if args.no_words:
                handle_missing_words(works_files, dictionary_words, out)

            if args.frequencies:
                handle_frequencies(works_files, args.frequencies, out)

if __name__ == "__main__":
    main()
