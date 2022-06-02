import re
import json
import glob
from collections import defaultdict
from tqdm import tqdm


def to_pos_sequence(items):
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


class Corpus:
    def __init__(self, root='corpora/*.json'):
        self.files = glob.glob(root)
        if isinstance(self.files, str):
            self.files = [self.files]

        # data
        self.ids = list()
        self.texts = defaultdict(str)
        self.morphemes = defaultdict(str)

        # search index & statistics
        self.raw_index = defaultdict(list)
        self.pos_index = defaultdict(list)
        self.stats = dict(sentences=0, eojeols=0, tokens=0, types=0)

        # preprocessing
        self._load_corpus()
        self._indexing()

    def _load_corpus(self):
        for file in tqdm(self.files, desc=f'Loading {len(self.files)} files...'):
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
                            self.stats['eojeols'] += len(snt['word'])
                            self.stats['tokens'] += len(snt['morpheme'])
                            self.stats['types'] += len(set([_t['form'] + '/' + _t['label'] for _t in snt['morpheme']]))

    def _indexing(self):
        for key in tqdm(self.ids, desc=f'Indexing {len(self.ids)} data...'):
            for w_i, w in enumerate(self.texts[key].split()):
                self.raw_index[w].append((key, w_i))
            for p_i, p in enumerate(self.morphemes[key].split()):
                self.pos_index[p].append((key, p_i))
        print(self.stats)
        print('Size of raw_word_index:', len(self.raw_index))
        print('Size of pos_word_index:', len(self.pos_index))

    def search(self, query, window_size=5):
        results = []
        counts = defaultdict(int)
        for target in self.pos_index.keys():
            if re.findall(query, target):
                results.append((target, self.pos_index[target]))
                counts[target] += len(self.pos_index[target])
        hit = 1
        for target, indices in results:
            for idx in indices:
                snt_id, word_id = idx
                text = self.morphemes[snt_id]
                splits = text.split()
                left = splits[:word_id]
                if len(left) > window_size:
                    left = ['⋯'] + left[-window_size:]
                center = splits[word_id]
                right = splits[word_id + 1:]
                if len(right) > window_size:
                    right = right[:window_size] + ['⋯']

                # formatted printing
                print(f"{str(hit).ljust(6)}"
                      f"\t{str(idx).ljust(50)}"
                      '\t\033[96m ' + target + '\033[0m\t'
                      f"{' '.join(left).rjust(40)} "
                      '\033[38;2;215;95;215m' + center + '\033[0m' +
                      f" {' '.join(right).ljust(40)}")

                hit += 1
        print('Top-10 Freq:', sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10])
        print('Query:', '\033[31m' + query + '\033[0m')


if __name__ == '__main__':
    corpus = Corpus(root='corpora/*.json')
    for _ in range(10):
        keyword = input('\n\n검색: ')
        corpus.search(query=keyword)
