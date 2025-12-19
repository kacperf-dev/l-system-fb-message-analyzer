import json
import os

from src.analysis.SentimentAnalyzer import SentimentAnalyzer
from src.generators.TreeDataGenerator import TreeDataGenerator
from src.utils import loaders


def main():
    print("[1/3] Loading conversation data...")
    conversation_data = loaders.load_message_data("data/")

    print("[2/3] Analyzing sentiment...")
    sentiment_analyzer = SentimentAnalyzer()
    messages_with_sentiment = sentiment_analyzer.analyze(conversation_data)

    print("[3/3] Generating tree data...")
    tree_generator = TreeDataGenerator()
    tree_data = tree_generator.generate_tree_data(messages_with_sentiment)

    if not os.path.exists("out"):
        os.makedirs("out")

    with open("out/tree_data.json", "w") as f:
        json.dump(tree_data, f, indent=4)

    print("Success! Tree data saved to out/tree_data.json")


if __name__ == "__main__":
    main()