from wordcloud import WordCloud
from rake_nltk import Rake
import random
import string
import os

WORDCLOUD_FOLDER = f"{os.getcwd()}/uploaded_files/wordclouds"
RX_WORDCLOUD_FOLDER = "wordclouds"


def generate_random_string(length: int) -> str:
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


class WordCloudGenerator:
    def __init__(self):
        self.rake = Rake()

    def generate_word_cloud(self, text: str) -> str:
        self.rake.extract_keywords_from_text(text)
        keywords = self.rake.get_ranked_phrases()
        wordcloud = WordCloud(height=480, width=640, max_words=20).generate(
            " ".join(keywords)
        )

        suffix = generate_random_string(10)
        save_path = f"{WORDCLOUD_FOLDER}/wordcloud_{suffix}.png"
        wordcloud.to_file(save_path)
        return f"{RX_WORDCLOUD_FOLDER}/wordcloud_{suffix}.png"
