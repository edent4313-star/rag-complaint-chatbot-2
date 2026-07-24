# RAG Complaint Chatbot 
CFPB Complaint Analysis RAG Chatbot
Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system for analyzing Consumer Financial Protection Bureau (CFPB) complaint data. The system enables users to ask natural language questions about customer complaints and receive context-aware answers generated using Large Language Models (LLMs) and semantic search.

The project covers the complete RAG workflow:

Exploratory Data Analysis (EDA)
Data Cleaning and Preprocessing
Text Chunking
Embedding Generation
Vector Store Indexing with FAISS
Retrieval-Augmented Generation (RAG)
Interactive Chat Interface using Gradio
Project Structure


The dataset contains consumer complaints submitted to financial institutions regarding products and services such as:

Credit Cards
Personal Loans
Savings Accounts
Money Transfers

For this project, only these four categories were retained and standardized.

Task 1: Exploratory Data Analysis and Preprocessing
Objectives
Analyze complaint distribution across products
Measure narrative lengths
Identify missing narratives
Clean and normalize complaint text
Preprocessing Steps
Convert text to lowercase
Remove special characters
Remove CFPB redaction tokens (e.g., XXXX)
Remove boilerplate phrases
Remove extra whitespace
Output
data/filtered_complaints.csv
Task 2: Text Chunking, Embedding and Vector Indexing
Sampling Strategy

A stratified sample was created to preserve the proportional distribution of complaint categories.

Chunking

LangChain RecursiveCharacterTextSplitter was used with:

chunk_size = 500
chunk_overlap = 100
Embedding Model
sentence-transformers/all-MiniLM-L6-v2

Reasons for selection:

Fast inference
Strong semantic similarity performance
Lightweight and efficient
Widely used in RAG systems
Vector Database

FAISS was used for similarity search and vector indexing.

Outputs
vector_store/faiss_index.bin
vector_store/metadata.pkl
