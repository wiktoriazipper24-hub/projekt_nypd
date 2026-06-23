"""Cosine similarity criterion for comparing writing styles between literary works."""

import numpy as np
from analyzer.stats import get_top_n_words

stop_words = {
    'i', 'w', 'na', 'z', 'do', 'nie', 'się', 'to', 'że', 'a', 'jest',
    'jak', 'o', 'ale', 'co', 'tak', 'by', 'czy', 'po', 'dla', 'go',
    'być', 'ten', 'która', 'który', 'które', 'gdy', 'już', 'tylko',
    'jego', 'ja', 'ty', 'on', 'ona', 'my', 'wy', 'oni', 'tu', 'tam', 'za', 
    'od', 'był','przez', 'pod', 'mu', 'and', 'the', 'of', 'or', 'gutenberg',
    'project', 'in', 'you', 'with', 'u', 'ich', 'str', 'work'
}


def calculate_cosine_similarity(counter1, counter2, n=1000):
    """Calculates style similarity between two texts (0-100) using cosine similarity
    on frequency vectors of their top-n most frequent words, excluding stop words."""
    top_words_1 = {word for word, _ in get_top_n_words(counter1, n)}
    top_words_2 = {word for word, _ in get_top_n_words(counter2, n)}

    vocabulary = list((top_words_1 | top_words_2) - stop_words)

    if not vocabulary:
        return 0.0

    vec1 = np.array([counter1.get(word, 0) for word in vocabulary])
    vec2 = np.array([counter2.get(word, 0) for word in vocabulary])

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = dot_product / (norm1 * norm2)
    return round(similarity * 100, 2)
