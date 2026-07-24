import pandas as pd

from config import DATA_PATH


class DashboardService:

    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)

    def get_kpis(self):

        return {

            "total_complaints": len(self.df),

            "products": self.df["product"].nunique(),

            "companies": self.df["company"].nunique(),

            "states": self.df["state"].nunique(),

            "average_length": round(

                self.df["consumer_complaint_narrative"]

                .str.split()

                .str.len()

                .mean(),

                2

            )

        }

    def product_distribution(self):

        return (

            self.df["product"]

            .value_counts()

            .reset_index()

            .rename(

                columns={

                    "index":"product",

                    "product":"count"

                }

            )

            .to_dict(

                orient="records"

            )

        )

    def top_issues(self):

        return (

            self.df["issue"]

            .value_counts()

            .head(10)

            .reset_index()

            .rename(

                columns={

                    "index":"issue",

                    "issue":"count"

                }

            )

            .to_dict(

                orient="records"

            )

        )

    def top_companies(self):

        return (

            self.df["company"]

            .value_counts()

            .head(10)

            .reset_index()

            .rename(

                columns={

                    "index":"company",

                    "company":"count"

                }

            )

            .to_dict(

                orient="records"

            )

        )

    def monthly_trend(self):

        df = self.df.copy()

        df["date_received"] = pd.to_datetime(df["date_received"])

        df["month"] = df["date_received"].dt.to_period("M").astype(str)

        return (

            df.groupby("month")

            .size()

            .reset_index(name="count")

            .to_dict(orient="records")

        )