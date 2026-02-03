from strsimpy.cosine import Cosine
from strsimpy.levenshtein import Levenshtein

def cos_similarity(t1: str, t2: str) -> float:
    _cos = Cosine(2)
    return _cos.similarity(t1, t2)

def levenshtein_distance(t1: str, t2: str) -> float:
    _lev = Levenshtein()
    return _lev.distance(t1, t2)


if __name__ == '__main__':
    print(levenshtein_distance("X-RAY", "XRAY"))

