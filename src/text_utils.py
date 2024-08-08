from wordcloud import WordCloud
from rake_nltk import Rake
import random
import string
import os
import yake

WORDCLOUD_MAX_WORDS = 10
WORDCLOUD_FOLDER = f"{os.getcwd()}/uploaded_files/wordclouds"
RX_WORDCLOUD_FOLDER = "wordclouds"


def generate_random_string(length: int) -> str:
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


class WordCloudGenerator:
    def __init__(self):
        self.rake = Rake()
        self.kw_extractor = yake.KeywordExtractor(
            lan="en", n=2, top=WORDCLOUD_MAX_WORDS
        )

    def generate_word_cloud(self, text: str) -> str:
        os.makedirs(WORDCLOUD_FOLDER, exist_ok=True)

        # self.rake.extract_keywords_from_text(text)
        # keywords = self.rake.get_ranked_phrases()
        keywords = self.kw_extractor.extract_keywords(text)
        wordcloud_input = {kw: (1 - score) for kw, score in keywords}

        # wordcloud = WordCloud(
        #     height=480, width=640, max_words=WORDCLOUD_MAX_WORDS
        # ).generate(" ".join(keywords))
        wordcloud = WordCloud(
            height=480, width=640, max_words=WORDCLOUD_MAX_WORDS
        ).generate_from_frequencies(wordcloud_input)

        suffix = generate_random_string(10)
        save_path = f"{WORDCLOUD_FOLDER}/wordcloud_{suffix}.png"
        wordcloud.to_file(save_path)
        return f"{RX_WORDCLOUD_FOLDER}/wordcloud_{suffix}.png"


def preprocess_bullet(bullet: str) -> str:
    bullet = bullet.strip("•")
    bullet = bullet.strip("*")
    bullet = bullet.strip(" ")
    return bullet
