from wordcloud import WordCloud
from rake_nltk import Rake
import random
import string

WORDCLOUD_FOLDER = "/home/jobin/Projects/TaSeSum/uploaded_files/wordclouds"
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
        wordcloud = WordCloud().generate(" ".join(keywords))

        suffix = generate_random_string(10)
        save_path = f"{WORDCLOUD_FOLDER}/wordcloud_{suffix}.png"
        wordcloud.to_file(save_path)
        return f"{RX_WORDCLOUD_FOLDER}/wordcloud_{suffix}.png"
