import torch
from transformers import pipeline
import pandas as pd


class SentimentAnalyzer:
    """
    Analyzes sentiment of messages
    """
    def __init__(self, model_name: str = "bardsai/twitter-sentiment-pl-base"):
        """
        Initializes sentiment analyzer engine
        :param model_name -- model chosen for sentiment analysis
        """
        self.device = 0 if torch.cuda.is_available() else -1
        print(f"Initializing model {model_name} on device {"GPU" if self.device == 0 else "CPU"}")
        self.analyzer = pipeline(
            task="text-classification",
            model=model_name,
            device=self.device
        )


    def analyze(self, conversation_data: pd.DataFrame, batch_size: int = 64) -> pd.DataFrame:
        """
        Runs sentiment analysis on messages in a conversation
        :param conversation_data -- Dataframe containing messages and metadata
        :param batch_size -- batch size used for sentiment analysis
        :return -- input DataFrame with added sentiment name, certainty and sentiment score columns
        """
        messages = list(conversation_data["message"])
        conversation_data.reset_index(drop=True, inplace=True)
        sentiment_df = pd.DataFrame(self.analyzer(messages, batch_size=batch_size))
        sentiment_df.rename(columns={"label": "sentiment", "score": "certainty"}, inplace=True)
        conversation_data = conversation_data.join(sentiment_df)

        conversation_data["sentiment_score"] = 0.5
        is_pos = (conversation_data["sentiment"] == "positive") & (conversation_data["is_analyzable"])
        is_neg = (conversation_data["sentiment"] == "negative") & (conversation_data["is_analyzable"])

        conversation_data.loc[is_pos, "sentiment_score"] = conversation_data["certainty"]
        conversation_data.loc[is_neg, "sentiment_score"] = 1 - conversation_data["certainty"]

        return conversation_data
