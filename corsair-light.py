import re
import json
import glob
import argparse
from collections import defaultdict
from itertools import cycle

try:
    from tqdm import tqdm
except ModuleNotFoundError as e:
    print('[Corsair] Need to install requirements. Type "pip install tqdm" on your terminal and retry.')
    raise e


class Colors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    NORMAL = '\033[0m'
    RAINBOW = [BRIGHT_YELLOW, BRIGHT_GREEN, BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_RED, BRIGHT_CYAN]

    @staticmethod
    def rainbow(items):
        return [color + it + Colors.NORMAL for it, color in zip(items, cycle(Colors.RAINBOW))]


def to_pos_sequence(items: list):
    """
    :param: items: list of dict objects from 'morpheme'
    :return: str sequence of part-of-speech tagging
    """
    word_id, word_buffer, sentence_buffer = 1, [], []
    try:
        for item in items:
            if item['word_id'] == word_id:
                word_buffer.append(f"{item['form']}/{item['label']}")
            else:
                word_id = item['word_id']
                sentence_buffer.append('+'.join(word_buffer))
                word_buffer = list()
                word_buffer.append(f"{item['form']}/{item['label']}")
        sentence_buffer.append('+'.join(word_buffer))
        return ' '.join(sentence_buffer)
    except TypeError:
        return None


def ngrams(items: list, n: int):
    assert 0 < n, 'incorrect `n` value.'
    results = []
    for start in range(len(items) - n + 1):
        end = start + n
        n_gram = items[start:end]
        if n_gram:
            results.append(n_gram)
    return results


class Corpus:
    def __init__(self, filepaths='corpora/*.json', ngram_window_size=5):
        self.files = glob.glob(filepaths)
        self.ngram_window_size = ngram_window_size

        # data
        self.snt_ids = set()
        self.texts = defaultdict(str)  # {"snt_id1": "이것은 문장입니다.", ...}
        self.pos_seqs = defaultdict(str)  # {"snt_id1": "이것/NP+은/JX 문장/NNG...", ...}

        # search index & statistics
        self.pos_ngram_keys = defaultdict(set)  # {1: {("형태소/NNG+를/JKO"), ...}, 2: {("형태소/NNG+를/JKO", "분석/NNG"), ...}}
        self.pos_ngram_index = defaultdict(list)  # {("형태소/NNG+를/JKO", "분석/NNG"): {"snt_id1", "snt_id2", ...}}
        self.stats = dict(sentences=0, words=0, tokens=0, ngrams=defaultdict(int))

        # preprocessing
        self.load_corpus()
        self.indexing()

    def load_corpus(self):
        for file in self.files:
            with open(file, encoding='utf-8') as f:
                filename = './' + file.rsplit(sep='\\')[-1]
                for doc in tqdm(json.load(f)['document'], desc=f'[Corsair] Loading "{filename}"...', ncols=100):
                    for snt in doc['sentence']:
                        if snt['word'] and snt['morpheme']:
                            snt_id = filename + '/' + snt['id']
                            self.snt_ids.add(snt_id)
                            self.texts[snt_id] = snt['form']
                            self.pos_seqs[snt_id] = to_pos_sequence(snt['morpheme'])
                            self.stats['sentences'] += 1
                            self.stats['words'] += len(snt['word'])
                            self.stats['tokens'] += len(snt['morpheme'])

    def indexing(self):
        for snt_id in tqdm(self.snt_ids, desc=f'[Corsair] Indexing {len(self.snt_ids)} data...', ncols=100):
            for n in range(1, self.ngram_window_size):
                for n_gram in ngrams(self.pos_seqs[snt_id].split(), n):
                    n_gram_key = tuple(n_gram)
                    self.pos_ngram_keys[n].add(n_gram_key)
                    self.pos_ngram_index[n_gram_key].append(snt_id)
                    self.stats['ngrams'][n] += 1

    def search(self, queries: list, topk: int = 25):
        search_space = self.pos_ngram_keys[len(queries)]
        accepted = set()
        for target in search_space:
            if all([re.search(q, w) for w, q in zip(target, queries)]):
                accepted.add(target)
        results = sorted([(t, self.pos_ngram_index[t]) for t in accepted], key=lambda x: len(x[1]), reverse=True)
        for target, snt_ids in results[:topk]:
            print(f'📑{len(snt_ids):4d}:\t{" ".join(Colors.rainbow(target))}')
        print(f'\n- only top {topk} results are displayed. found {len(results)} matches for {len(queries)} length items.')

    def query(self, user_input_str: str):
        query_items = user_input_str.split()
        if not any(query_items) or len(query_items) > self.ngram_window_size:
            print(f'😅 wrong query - try again except: {query_items}')
        else:
            self.search(query_items)


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='A lightweight concordance tool for NIKL "Modu" Corpora: modified for simpler pattern finding.'
    )

    # args
    p.add_argument('--dir', type=str, default='corpora/*.json')
    p.add_argument('--ngram_window_size', type=int, default=5)

    args = p.parse_args()
    corpus = Corpus(filepaths=args.dir, ngram_window_size=args.ngram_window_size)

    while True:
        try:
            user_input = input('\n[Corsair:POS] >> ')
            if user_input == '-quit' or user_input == '-exit':
                raise EOFError
            corpus.query(user_input_str=user_input)
        except re.error as e:
            print('[Corsair] re.error:', e)
        except EOFError as e:
            break

    print('[Corsair] Exit...')
