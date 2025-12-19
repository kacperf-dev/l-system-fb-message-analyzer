from src.utils import loaders
import pandas as pd


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    data = loaders.load_message_data('data')
    print(data)

if __name__ == "__main__":
    main()