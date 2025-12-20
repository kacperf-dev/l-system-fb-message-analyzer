import torch
from transformers import pipeline
import pandas as pd
from tqdm import tqdm


class SentimentAnalyzer:
    """
    Analyzes sentiment of messages
    """
    def __init__(self, model_name: str = "bardsai/twitter-sentiment-pl-base", batch_size: int = 32):
        """
        Initializes sentiment analyzer engine
        :param model_name -- model chosen for sentiment analysis
        """
        self.device = 0 if torch.cuda.is_available() else -1
        print(f"Initializing model {model_name} on device {"GPU" if self.device == 0 else "CPU"}")
        self.batch_size = batch_size
        self.analyzer = pipeline(
            task="text-classification",
            model=model_name,
            device=self.device,
            batch_size=self.batch_size
        )


    def analyze(self, conversation_data: pd.DataFrame) -> pd.DataFrame:
        """
        Runs sentiment analysis on messages in a conversation
        :param conversation_data -- Dataframe containing messages and metadata
        :return -- input DataFrame with added sentiment name, certainty and sentiment score columns
        """
        analyzable_mask = conversation_data["is_analyzable"] == True
        to_analyze = conversation_data[analyzable_mask].copy()

        if to_analyze.empty:
            conversation_data["sentiment_score"] = 0.5
            return conversation_data

        messages = to_analyze["message"].tolist()
        results = []

        print(f"Analyzing {len(messages)} messages (Batch size: {self.batch_size})...")

        for i in tqdm(range(0, len(messages), self.batch_size), desc="Sentiment Analysis"):
            batch = messages[i:i+self.batch_size]
            batch_results = self.analyzer(batch, truncation=True, padding=True)
            results.extend(batch_results)

        res_df = pd.DataFrame(results)

        def map_score(row):
            label = row["label"].lower()
            cert = row["score"]

            if label == "positive": return 0.5 + (cert * 0.5)
            if label == "negative": return 0.5 - (cert * 0.5)
            return 0.5

        to_analyze["sentiment_label"] = res_df["label"].values
        to_analyze["certainty"] = res_df["score"].values
        to_analyze["sentiment_score"] = res_df.apply(map_score, axis=1).values

        conversation_data["sentiment_label"] = "neutral"
        conversation_data["certainty"] = 0.0
        conversation_data["sentiment_score"] = 0.5

        conversation_data.update(to_analyze[["sentiment_label", "certainty", "sentiment_score"]])

        return conversation_data
