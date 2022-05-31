import json
import glob
from collections import defaultdict
from tqdm import tqdm


def to_pos_sequence(items):
    word_id = 1
    word_buffer = []
    sentence_buffer = []
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
        self.ids = list()
        self.texts = defaultdict(str)
        self.morphemes = defaultdict(str)
        self.alignments = defaultdict(list)

        self._load_files(root=root)

    def _load_files(self, root):
        files = glob.glob(root)[-1]  # 마지막 파일만 load
        if isinstance(files, str):
            files = [files]
        for file in tqdm(files):
            with open(file, encoding='utf-8') as f:
                for doc in json.load(f)['document']:
                    for sentence in doc['sentence']:
                        key = sentence['id']
                        self.ids.append(key)
                        self.texts[key] = sentence['form']
                        self.morphemes[key] = to_pos_sequence(sentence['morpheme'])


if __name__ == '__main__':
    corpus = Corpus(root='corpora/*.json')
    for i in range(10):
        k = corpus.ids[i]
        print(corpus.texts[k])
        print(corpus.morphemes[k])
