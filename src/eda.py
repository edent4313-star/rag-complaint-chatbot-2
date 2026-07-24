import matplotlib.pyplot as plt

def plot_product_distribution(df):

    product_counts = (
        df["Product"]
        .value_counts()
        .head(15)
    )

    product_counts.plot(
        kind="bar",
        figsize=(10,6)
    )

    plt.title("Complaint Distribution by Product")
    plt.tight_layout()
    plt.show()


def narrative_length_analysis(df):

    narrative_col = "Consumer complaint narrative"

    df["word_count"] = (
    df[narrative_col]
        .fillna("")
        .str.split()
        .str.len()
    )

    print(df["word_count"].describe())

    return df

def narrative_presence_analysis(df):

    narrative_col = "Consumer complaint narrative"

    with_text = (
        df[narrative_col]
        .notna()
        .sum()
    )

    without_text = (
        df[narrative_col]
        .isna()
        .sum()
    )

    print("With Narrative:", with_text)
    print("Without Narrative:", without_text)