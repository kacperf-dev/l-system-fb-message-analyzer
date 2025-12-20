import os
import pandas as pd

from src.analysis.SentimentAnalyzer import SentimentAnalyzer
from src.generators.TreeDataGenerator import TreeDataGenerator
from src.services.LSystemGenerator import LSystemGenerator
from src.utils.loaders import load_message_data


def main():
    DATA_DIR = "data/"
    CACHE_PATH = "out/sentiment_cache.csv"
    OUTPUT_PATH = "out/tree_word.txt"

    os.makedirs("out", exist_ok=True)

    if os.path.exists(CACHE_PATH):
        print(f"--- [CACHE] Found processed data: {CACHE_PATH} ---")
        df = pd.read_csv(CACHE_PATH, parse_dates=["send_datetime"])
    else:
        print(f"--- [1/3] Loading raw data from {DATA_DIR} ---")
        df = load_message_data(DATA_DIR)

        print(f"--- [2/3] Analyzing sentiment ---")
        analyzer = SentimentAnalyzer(batch_size=64)
        df = analyzer.analyze(df)

        print(f"--- [CACHE] Saving analysis results to {CACHE_PATH} ---")
        df.to_csv(CACHE_PATH, index=False)

    print("--- [3/3] Generating tree hierarchy and L-system word ---")
    tree_data = TreeDataGenerator.generate_tree_data(df, contrast=2.5)
    lsystem = LSystemGenerator(tree_data)
    word = lsystem.generate()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(word)

    print(f"Success! L-system word saved to {OUTPUT_PATH}")
    print(f"Number of analyzed months: {tree_data['meta']['total_months']}")
    print(f"Calculated trunk height: {tree_data['meta']['trunk_height']}")


if __name__ == "__main__":
    main()