import json
import os

from src.analysis.SentimentAnalyzer import SentimentAnalyzer
from src.generators.TreeDataGenerator import TreeDataGenerator
from src.utils import loaders


def main():
    sentiment_analyzer = SentimentAnalyzer()
    tree_generator = TreeDataGenerator()

    conversation_data = loaders.load_message_data("data/")
    messages_with_sentiment = sentiment_analyzer.analyze(conversation_data)
    tree_data = tree_generator.generate_tree_data(messages_with_sentiment)

    if not os.path.exists("out"):
        os.makedirs("out")

    with open("out/tree_data.json", "w") as f:
        json.dump(tree_data, f, indent=4)


if __name__ == "__main__":
    main()