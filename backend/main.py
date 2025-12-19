from src.analysis.SentimentAnalyzer import SentimentAnalyzer
from src.utils import loaders


def main():
    conversation_data = loaders.load_message_data("data/")

    sentiment_analyzer = SentimentAnalyzer()
    messages_with_sentiment = sentiment_analyzer.analyze(conversation_data)

    print(messages_with_sentiment)


if __name__ == "__main__":
    main()