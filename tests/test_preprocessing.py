
import src
from src.preprocessing import clean_text

def test_clean_text():

    text = "I AM WRITING TO FILE A COMPLAINT!!!"

    cleaned = clean_text(text)

    assert "complaint" in cleaned
