import re
import pandas as pd

'''def filter_products(df, products):

    return df[
        df["Product"]
        .isin(products)
    ]'''

product_map = {
    "credit_card": [
        "Credit card",
        "Credit card or prepaid card"
    ],
    "personal_loan": [
        "Payday loan, title loan, personal loan, or advance loan",
        "Payday loan, title loan, or personal loan",
        "Consumer Loan"
    ],
    "savings_products": [
        "Checking or savings account",
        "Bank account or service"
    ],
    "money_transfer": [
        "Money transfer, virtual currency, or money service",
        "Money transfers"
    ]
}

def filter_products(df, combined_list):
    return df[df["Product"].isin(combined_list)]


def filter_by_groups(df, group_keys):
    combined = []
    for key in group_keys:
        combined.extend(product_map[key])
    return filter_products(df, combined)
def remove_empty_narratives(df):

    col = "Consumer complaint narrative"

    return df[
        df[col].notna()
    ]

def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # Remove byte-string prefix
    text = re.sub(r"^b['\"]", "", text)

    # Lowercase
    text = text.lower()

    text = re.sub(r'\bx+\b', ' ', text)

    # Remove common boilerplate
    boilerplate_patterns = [
        r"i am writing to file a complaint",
        r"i am writing to dispute",
        r"dear cfpb",
        r"to whom it may concern",
        r"i would like to report"
    ]

    for pattern in boilerplate_patterns:
        text = re.sub(pattern, "", text)

    # Remove special characters
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()