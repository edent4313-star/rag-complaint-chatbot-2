import src
def test_embedding_dimension():

    assert src.embeddings.shape[1] == 384
