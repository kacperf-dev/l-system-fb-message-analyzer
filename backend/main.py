import json
import os

from src.analysis.SentimentAnalyzer import SentimentAnalyzer
from src.generators.TreeDataGenerator import TreeDataGenerator
from src.services.LSystemGenerator import LSystemGenerator
from src.utils import loaders


def main():
    print("[1/4] Loading conversation data...")
    conversation_data = loaders.load_message_data("data/")

    print("[2/4] Analyzing sentiment...")
    sentiment_analyzer = SentimentAnalyzer()
    messages_with_sentiment = sentiment_analyzer.analyze(conversation_data)

    print("[3/4] Generating tree data...")
    tree_generator = TreeDataGenerator()
    tree_data = tree_generator.generate_tree_data(messages_with_sentiment)

    if not os.path.exists("out"):
        os.makedirs("out")

    with open("out/tree_data.json", "w") as f:
        json.dump(tree_data, f, indent=4)

    print("Success! Tree data saved to out/tree_data.json")

    print("[4/4] Compilin L-system word...")
    lsystem = LSystemGenerator(tree_data)
    tree_word = lsystem.generate()

    with open("out/tree_word.txt", "w") as f:
        f.write(tree_word)

    with open("../frontend/public/tree_word.txt", "w") as f:
        f.write(tree_word)

    print("Success! Tree word saved to out/tree_word.txt and frontend/public/tree_word.txt")


if __name__ == "__main__":
    main()