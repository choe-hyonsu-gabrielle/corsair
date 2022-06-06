import re
import json
import glob
import datetime
import argparse
from collections import defaultdict

try:
    from tqdm import tqdm
    from openpyxl import Workbook
except ModuleNotFoundError as e:
    print('[Corsair: raw-only] Need to install requirements. Type "pip install tqdm openpyxl" on your terminal and retry.')
    raise e


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
        f"{filename.ljust(25)}{doc_id.ljust(23)}{str(w_idx+1).ljust(3)}"
        '\033[38;2;215;95;215m' + target + '\033[0m  '
        f"{' '.join(left).rjust(25)} "
        '\033[38;2;215;95;215m' + center + '\033[0m'
        f" {' '.join(right).ljust(25)}"
    )


def _export_to_xlsx(data):
    export_to = 'corsair_export-' + datetime.datetime.now().strftime('%Y-%m-%d-%H.%M.%S') + '.xlsx'
    wb = Workbook()
    ws = wb.active
    ws.append(('hits', 'filename', 'doc_id', 'word_idx', 'target', 'left', 'center', 'right'))
    for row_idx, values in enumerate(data):
        # values = (hit, key, left, center, right, map_left, map_center, map_right)
        hit = values[0]
        (filename, doc_id), w_idx = values[1][0].rsplit('/', maxsplit=1), values[1][1] + 1
        mapped_target = values[3] + f' ({values[6]})'
        left, center, right = ' '.join(values[2]), values[3], ' '.join(values[4])
        row = (hit, filename, doc_id, w_idx, mapped_target, left, center, right)
        ws.append(row)
    wb.save(filename=export_to)
    return export_to


class Corpus:
    def __init__(self, root='corpora/*.json', window_size=5, map_window_size=2):
        self.files = glob.glob(root)
        self.files = [self.files] if isinstance(self.files, str) else self.files
        self.window_size = window_size
        self.map_window_size = map_window_size

        # data
        self.ids = list()
        self.texts = defaultdict(str)

        # search index & statistics
        self.raw_unigram_index = defaultdict(list)
        self.raw_bigram_index = defaultdict(list)
        self.pos_unigram_index = defaultdict(list)
        self.pos_bigram_index = defaultdict(list)
        self.stats = dict(sentences=0, words=0)

        # preprocessing
        self._load_corpus()
        self._indexing()

    def _load_corpus(self):
        for file in tqdm(self.files, desc=f'[Corsair: raw-only] Loading {len(self.files)} files...', ncols=100):
            with open(file, encoding='utf-8') as f:
                filename = './' + file.rsplit(sep='\\')[-1]
                for doc in json.load(f)['document']:
                    for snt in doc['sentence']:
                        if snt['form']:
                            key = filename + '/' + snt['id']
                            self.ids.append(key)
                            self.texts[key] = snt['form']
                            self.stats['sentences'] += 1
                            self.stats['words'] += len(snt['word'])

    def _indexing(self):
        for key in tqdm(self.ids, desc=f'[Corsair: raw-only] Indexing {len(self.ids)} data...', ncols=100):
            for w_i, w in enumerate(self.texts[key].split()):
                self.raw_unigram_index[w].append((key, w_i))
            for wh_i, w2 in enumerate(zip(self.texts[key].split(), self.texts[key].split()[1:])):
                self.raw_bigram_index[' '.join(w2)].append((key, wh_i))
        print(self.stats)
        print(dict(raw_unigram_index=len(self.raw_unigram_index), raw_bigram_index=len(self.raw_bigram_index)))

    def _search(self, query, index=None, space=None, xlsx=False):
        n_gram_len = len(query)
        query = ' '.join(query)
        results = []
        counts = defaultdict(int)
        for ngram in index.keys():
            if re.findall(query, ngram):
                results.append((ngram, index[ngram]))
                counts[ngram] += len(index[ngram])
        hit = 1
        xlsx_data = []
        for target, indices in results:
            for key in indices:
                snt_id, word_id = key
                # On target search space
                splits = space[snt_id].split()
                left = splits[:word_id]
                center = ' '.join(splits[word_id:word_id + n_gram_len])
                right = splits[word_id + n_gram_len:]
                if self.window_size:
                    left_p = ['⋯'] + left[-self.window_size:] if len(left) > self.window_size else left
                    right_p = right[:self.window_size] + ['⋯'] if len(right) > self.window_size else right

                formatted_print(hit, key, target, left_p, center, right_p)
                if xlsx:
                    xlsx_data.append((hit, key, left, center, right))
                hit += 1
        print('[Corsair: raw-only] Query:', '\033[31m' + query + '\033[0m', f"({hit-1} results)")
        if counts:
            print('[Corsair: raw-only] Top-10 frequency:', sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10], '⋯')
        if counts and xlsx:
            exported_to = _export_to_xlsx(xlsx_data)
            print(f'[Corsair: raw-only] Saved {hit-1} results to file: "{exported_to}"')

    def command(self, command):
        action, *query = command.split(sep=' ')
        if action == '-raw' and len(query) == 1:
            self._search(query=query, index=self.raw_unigram_index, space=self.texts)
        elif action == '-raw' and len(query) == 2:
            self._search(query=query, index=self.raw_bigram_index, space=self.texts)
        elif action == '-rawx' and len(query) == 1:
            self._search(query=query, index=self.raw_unigram_index, space=self.texts, xlsx=True)
        elif action == '-rawx' and len(query) == 2:
            self._search(query=query, index=self.raw_bigram_index, space=self.texts, xlsx=True)
        else:
            print("Wrong command: [-raw/-rawx] [primary expression] (secondary expression) or '-quit'")


def argument_parser():
    p = argparse.ArgumentParser(description='A lightweight concordance took for NIKL "Modu" Corpora.')
    # args
    p.add_argument('--dir', type=str, default='corpora/*.json')
    p.add_argument('--window_size', type=int, default=5)
    p.add_argument('--map_window_size', type=int, default=2)
    return p.parse_args()


if __name__ == '__main__':

    p = argparse.ArgumentParser(description='A lightweight concordance took for NIKL "Modu" Corpora.')

    # args
    p.add_argument('--dir', type=str, default='corpora/*.json')
    p.add_argument('--window_size', type=int, default=5)
    p.add_argument('--map_window_size', type=int, default=2)

    args = p.parse_args()
    corpus = Corpus(root=args.dir, window_size=args.window_size, map_window_size=args.map_window_size)

    while True:
        try:
            user_command = input('\n[Corsair: raw-only] >>> ')
            if user_command == '-quit':
                raise EOFError
            corpus.command(command=user_command)
        except re.error as e:
            print('[Corsair: raw-only] re.error:', e)
        except EOFError as e:
            break

    print('[Corsair: raw-only] Exit...')
