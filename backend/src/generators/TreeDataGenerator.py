import pandas as pd
import numpy as np


class TreeDataGenerator:
    """
    Aggregates sentiment data into structures used for L-system generation.
    """
    @staticmethod
    def _apply_contrast(value: float, factor: float = 2.0) -> None:
        """
        Stretches the sentiment score to emphasize differences
        :param value -- value to be contrasted
        :param factor -- factor by which to stretch the value
        :return
        """
        normalized = value - 0.5
        boosted = np.sign(normalized) * (np.abs(normalized * 2) ** (1 / factor)) / 2
        return boosted + 0.5


    @staticmethod
    def generate_tree_data(conversation_data: pd.DataFrame, freq: str = "W", contrast: float = 2.0) -> list:
        """
        Groups messages by year and month and calculates mean sentiment score as well as message count for each group
        :param conversation_data -- Dataframe containing messages and metadata
        :param freq -- frequency at which to group messages
        :return -- list of dicts containing tree data
        """
        grouped_stats = conversation_data.groupby(pd.Grouper(key="send_datetime", freq=freq)).agg(
            avg_sentiment=("sentiment_score", "mean"),
            msg_count=("message", "count")
        ).reset_index()

        grouped_stats = grouped_stats[grouped_stats["msg_count"] > 0].copy()
        grouped_stats["avg_sentiment"] = grouped_stats["avg_sentiment"].apply(
            lambda x: TreeDataGenerator._apply_contrast(x, factor=contrast)
        )
        grouped_stats["send_datetime"] = grouped_stats["send_datetime"].dt.strftime("%Y-%m-%d")

        return grouped_stats.to_dict(orient="records")