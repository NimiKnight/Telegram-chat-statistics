import json
from pathlib import Path

from arabic_reshaper import reshape
from hazm import Normalizer, word_tokenize
from loguru import logger
from src.data import DATA_DIR
from wordcloud import WordCloud


class ChatStatistics:

    normalizer = Normalizer()

    logger.info('Loading stop-words from src/data/persian_stop_words.txt')
    with open(DATA_DIR / 'persian_stop_words.txt') as f:
        stop_words = f.readlines()
        stop_words = set(map(str.strip, stop_words))
        stop_words = set(map(normalizer.normalize, stop_words))

    def __init__(self, json_path) -> None:
        with open(json_path) as f:
            self.data = json.load(f)

    def extract_text(self):
        logger.info('Extracting text from chat data...')
        text = ''
        for msg in self.data['messages']:
            if type(msg.get('text', None)) is str:
                text_tokens = word_tokenize(self.normalizer.normalize(msg['text']))
                text_tokens = list(filter(lambda word: word not in self.stop_words, text_tokens))
                text += ' '.join(text_tokens)
        return text

    def generate_word_cloud(self, output_dir):
        text = self.extract_text()
        text = reshape(text)
        logger.info("Generating Word Cloud...")
        wordcloud = WordCloud(
            font_path=str(DATA_DIR / 'NotoNaskhArabic-Regular.ttf'),
            width=3840,
            height=2160,
            background_color='white'
            ).generate(text)

        logger.info(f"Saving Word Cloud To {output_dir}")
        wordcloud.to_file(str(output_dir / 'result.png'))


if __name__ == '__main__':
    chat1 = ChatStatistics(DATA_DIR / 'result.json')
    chat1.generate_word_cloud(DATA_DIR)
    print('done!')
