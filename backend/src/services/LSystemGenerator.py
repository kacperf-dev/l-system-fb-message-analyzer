class LSystemGenerator:
    """
    Generates word following an L-system grammar.
    """
    def __init__(self, tree_hierarchy: list):
        self.tree_hierarchy = tree_hierarchy
        self.current_direction = -1


    def generate(self) -> str:
        """
        Main method initializing process of generating word. Iterates over every month.
        :return -- generated word
        """
        word = []
        for month_data in self.tree_hierarchy:
            word.append(self._produce_month(month_data))
            self.current_direction *= -1
        return "".join(word)

    def _produce_month(self, month_data: dict) -> str:
        """
        Generates a substring of the main word representing a single month. Each month is a branch containing subbranches representing weeks.
        Logic:
            1. Generate symbol T (vertical segment)
            2. Open branch structure [ with a direction sign
            3. Generate subbranches representing weeks
            4. Close branch structure ]
        :param month_data -- dict containing month data
        :return -- substring of the main word
        """
        h = 20
        sign = "+" if self.current_direction == 1 else "-"

        month_word = f"T({h})[{sign}]"
        for week in month_data["weeks"]:
            month_word += self._produce_week(week)
        month_word += "]"

        return month_word


    def _produce_week(self, week_data: dict) -> str:
        """
        Generates a substring representing a single week inside a month branch.
        Logic:
            1. Generates step M, positioning week on month axis.
            2. Creates a subbranhc W, representing week (length(msg_count) = 10 + (msg_count * 0.5)).
            3. Puts a terminal fruit symbol and the end.
        :param week_data:
        :return:
        """
        s = week_data["avg_sentiment"]
        m = week_data["msg_count"]

        w_len = 10 + (m * 0.5)

        return f"M(8)[+W({w_len:.1f})F({s:.2f},{m})]"