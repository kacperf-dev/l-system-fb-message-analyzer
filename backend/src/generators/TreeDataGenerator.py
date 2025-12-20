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
    def generate_tree_data(conversation_data: pd.DataFrame, contrast: float = 2.0) -> dict:
        """
        Groups messages by year and month and calculates mean sentiment score as well as message count for each group
        :param conversation_data -- Dataframe containing messages and metadata
        :param contrast -- factor by which to stretch the sentiment score
        :return -- list of dicts containing tree data
        """
        weekly_stats = conversation_data.groupby(pd.Grouper(key="send_datetime", freq="W")).agg(
            avg_sentiment=("sentiment_score", "mean"),
            msg_count=("message", "count")
        ).reset_index()

        weekly_stats = weekly_stats[weekly_stats["msg_count"] > 0].copy()

        weekly_stats["avg_sentiment"] = weekly_stats["avg_sentiment"].apply(
            lambda x: TreeDataGenerator._apply_contrast(x, factor=contrast)
        )

        weekly_stats["normalized_count"] = np.log1p(weekly_stats["msg_count"]) * 5.0
        weekly_stats["raw_count"] = weekly_stats["msg_count"].astype(int)

        weekly_stats["avg_sentiment"] = weekly_stats["avg_sentiment"].astype(float)
        weekly_stats["normalized_count"] = weekly_stats["normalized_count"].astype(float)
        weekly_stats["send_datetime"] = weekly_stats["send_datetime"].dt.strftime("%Y-%m-%d")
        weekly_stats["year_month"] = weekly_stats["send_datetime"].str[:7]

        max_tree_height = 600
        unique_months = weekly_stats["year_month"].nunique()

        trunk_segment_h = max_tree_height / (unique_months + 2)
        trunk_segment_h = max(10, min(trunk_segment_h, 40))

        tree_hierarchy = []
        for month, month_df in weekly_stats.groupby("year_month"):
            month_entry = {
                "month": month,
                "weeks": month_df.drop(columns=["year_month", "msg_count"]).to_dict(orient="records")
            }
            tree_hierarchy.append(month_entry)

        return {
            "meta": {
                "trunk_height": float(trunk_segment_h),
                "total_months": int(unique_months),
            },
            "months": tree_hierarchy
        }

