'''def create_stratified_sample(df, sample_size=12000):

    sample_fraction = sample_size / len(df)

    return (
        df.groupby("Product", group_keys=False)
        .sample(frac=sample_fraction, random_state=42)
        .reset_index(drop=True)
    )'''

def create_sample(df, sample_size=12000):

    sample_fraction = sample_size / len(df)

    return (
        df.sample(frac=sample_fraction, random_state=42)
        .reset_index(drop=True)
    )