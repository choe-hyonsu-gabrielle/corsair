import re
import json
import glob
from collections import defaultdict
from tqdm import tqdm


def to_pos_sequence(items):
    """
    :param items: list of dict objects from 'morpheme'
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


def formatted_print(hit, key, target, left, center, right):
    (filename, doc_id), w_idx = key[0].rsplit('/', maxsplit=1), key[1]
    print(
        f"{str(hit).ljust(6)}"
        f"{filename.ljust(25)}{doc_id.ljust(23)}{str(w_idx).ljust(3)}"
        '\033[96m ' + target.ljust(30) + '\033[0m'
        f"{' '.join(left).rjust(40)} "
        '\033[38;2;215;95;215m' + center + '\033[0m'
        f" {' '.join(right).ljust(40)}"
    )


class Corpus:
    def __init__(self, root='corpora/*.json'):
        self.files = glob.glob(root)
        if isinstance(self.files, str):
            self.files = [self.files]
        self.window_size = 5

        # data
        self.ids = list()
        self.texts = defaultdict(str)
        self.morphemes = defaultdict(str)

        # search index & statistics
        self.raw_unigram_index = defaultdict(list)
        self.raw_bigram_index = defaultdict(list)
        self.pos_unigram_index = defaultdict(list)
        self.pos_bigram_index = defaultdict(list)
        self.stats = dict(sentences=0, words=0, tokens=0, types=0)

        # preprocessing
        self._load_corpus()
        self._indexing()

    def _load_corpus(self):
        for file in tqdm(self.files, desc=f'[Corsair] Loading {len(self.files)} files...'):
            with open(file, encoding='utf-8') as f:
                filename = './' + file.rsplit(sep='\\')[-1]
                for doc in json.load(f)['document']:
                    for snt in doc['sentence']:
                        if snt['form'] and snt['morpheme']:
                            key = filename + '/' + snt['id']
                            self.ids.append(key)
                            self.texts[key] = snt['form']
                            self.morphemes[key] = to_pos_sequence(snt['morpheme'])
                            self.stats['sentences'] += 1
                            self.stats['words'] += len(snt['word'])
                            self.stats['tokens'] += len(snt['morpheme'])
                            self.stats['types'] += len(set([_t['form'] + '/' + _t['label'] for _t in snt['morpheme']]))

    def _indexing(self):
        for key in tqdm(self.ids, desc=f'[Corsair] Indexing {len(self.ids)} data...'):
            for w_i, w in enumerate(self.texts[key].split()):
                self.raw_unigram_index[w].append((key, w_i))
            for wh_i, w2 in enumerate(zip(self.texts[key].split(), self.texts[key].split()[1:])):
                self.raw_bigram_index[' '.join(w2)].append((key, wh_i))
            for p_i, p in enumerate(self.morphemes[key].split()):
                self.pos_unigram_index[p].append((key, p_i))
            for ph_i, p2 in enumerate(zip(self.morphemes[key].split(), self.morphemes[key].split()[1:])):
                self.pos_bigram_index[' '.join(p2)].append((key, ph_i))
        print(self.stats)
        print(dict(raw_unigram_index=len(self.raw_unigram_index), raw_bigram_index=len(self.raw_bigram_index),
                   pos_unigram_index=len(self.pos_unigram_index), pos_bigram_index=len(self.pos_bigram_index)))

    def _ngram_search(self, query, index=None, space=None, xlsx_export=False):
        ngram_len = len(query)
        query = ' '.join(query)
        results = []
        counts = defaultdict(int)
        for ngram in index.keys():
            if re.findall(query, ngram):
                results.append((ngram, index[ngram]))
                counts[ngram] += len(index[ngram])
        hit = 1
        for target, indices in results:
            for key in indices:
                snt_id, word_id = key
                seq = space[snt_id]
                splits = seq.split()
                left = splits[:word_id]
                center = ' '.join(splits[word_id:word_id + ngram_len])
                right = splits[word_id + ngram_len:]
                left_p, right_p = None, None
                if self.window_size:
                    left_p = ['⋯'] + left[-self.window_size:] if len(left) > self.window_size else left
                    right_p = right[:self.window_size] + ['⋯'] if len(right) > self.window_size else right
                formatted_print(hit, key, target, left_p, center, right_p)
                hit += 1
        print('Search query:', '\033[31m' + query + '\033[0m')
        if counts:
            print('Top-10 Freq:', sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10])

    def search(self, command):
        action, *query = command.split(sep=' ')
        if action == '-raw' and len(query) == 1:
            self._ngram_search(query=query, index=self.raw_unigram_index, space=self.texts)
        elif action == '-raw' and len(query) == 2:
            self._ngram_search(query=query, index=self.raw_bigram_index, space=self.texts)
        elif action == '-pos' and len(query) == 1:
            self._ngram_search(query=query, index=self.pos_unigram_index, space=self.morphemes)
        elif action == '-pos' and len(query) == 2:
            self._ngram_search(query=query, index=self.pos_bigram_index, space=self.morphemes)
        else:
            print("Wrong command: [-raw/-rawx/-pos/-posx] [head expression] (tail expression)")


if __name__ == '__main__':
    corpus = Corpus(root='corpora/*.json')
    for _ in range(10):
        keyword = input('\n[Corsair] command: ')
        corpus.search(command=keyword)


