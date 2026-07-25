import pandas as pd
from flask import jsonify

from config import DATA_PATH


class DashboardService:

    # Map the CSV's actual column names to clean internal names
    # Note: 'Product' is entirely null in filtered_complaints.csv;
    #       'Sub-product' holds the real product categories.
    _COL = {
        "narrative":    "Consumer complaint narrative",
        "product":      "Sub-product",
        "issue":        "Issue",
        "company":      "Company",
        "state":        "State",
        "date":         "Date received",
    }

    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)
        # Normalise column names to lowercase-stripped for safety
        self.df.columns = [c.strip() for c in self.df.columns]

    # ── helpers ───────────────────────────────────────────────────────────────
    def _col(self, key: str) -> str:
        """Return the actual column name, case-insensitive fallback."""
        target = self._COL[key]
        # Try exact match first, then case-insensitive
        if target in self.df.columns:
            return target
        for c in self.df.columns:
            if c.lower() == target.lower():
                return c
        raise KeyError(f"Column not found: {target!r}. Available: {list(self.df.columns)}")

    # ── endpoints ─────────────────────────────────────────────────────────────
    def get_kpis(self):
        narrative_col = self._col("narrative")
        narratives = self.df[narrative_col].fillna("").astype(str)
        word_counts = narratives.apply(lambda v: len(v.split()) if v else 0)

        return jsonify({
            "total_complaints": len(self.df),
            "products":         int(self.df[self._col("product")].nunique()),
            "companies":        int(self.df[self._col("company")].nunique()),
            "states":           int(self.df[self._col("state")].nunique()),
            "average_length":   round(float(word_counts.mean()), 2),
        })

    def product_distribution(self):
        col = self._col("product")
        counts = self.df[col].value_counts().reset_index()
        counts.columns = ["product", "count"]
        return jsonify(counts.to_dict(orient="records"))

    def top_issues(self):
        col = self._col("issue")
        counts = self.df[col].value_counts().head(10).reset_index()
        counts.columns = ["issue", "count"]
        return jsonify(counts.to_dict(orient="records"))

    def top_companies(self):
        col = self._col("company")
        counts = self.df[col].value_counts().head(10).reset_index()
        counts.columns = ["company", "count"]
        return jsonify(counts.to_dict(orient="records"))

    def monthly_trend(self):
        df = self.df.copy()
        date_col = self._col("date")
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col])
        df["month"] = df[date_col].dt.to_period("M").astype(str)

        result = (
            df.groupby("month")
            .size()
            .reset_index(name="count")
            .to_dict(orient="records")
        )
        return jsonify(result)
