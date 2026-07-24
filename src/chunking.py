from langchain_text_splitters import RecursiveCharacterTextSplitter

import pandas as pd

def create_chunks(df):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    
    records = []
    
    for _, row in df.iterrows():
        # Get the text and force it to be a string. 
        # If it is NaN/None, it becomes an empty string ""
        text = row["cleaned_narrative"]
        
        # Check if text is valid (not NaN and not empty)
        if not isinstance(text, str) or text.lower() == 'nan':
            continue  # Skip this row if there's no valid text
            
        complaint_id = row["Complaint ID"]
        product = row["Product"]
        
        chunks = splitter.split_text(text)
        
        for idx, chunk in enumerate(chunks):
            records.append({
                "complaint_id": complaint_id,
                "product": product,
                "chunk_id": idx,
                "chunk_text": chunk
            })
            
    return pd.DataFrame(records)

'''
def create_chunks(df):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    records = []

    for _, row in df.iterrows():

        complaint_id = row["Complaint ID"]

        product = row["Product"]

        text = row["cleaned_narrative"]

        chunks = splitter.split_text(text)

        for idx, chunk in enumerate(chunks):

            records.append({
                "complaint_id": complaint_id,
                "product": product,
                "chunk_id": idx,
                "chunk_text": chunk
            })

    return pd.DataFrame(records)'''