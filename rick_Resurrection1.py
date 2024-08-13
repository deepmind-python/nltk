# 必須用下列方式安裝下列：
# pip install --upgrade pdfminer.six
# pip install unstructured_pytesseract
# pip install pdf2image
# pip install pdfminer
# pip install opencv-python
# pip install pandas
# pip install langchain

from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain import HuggingFaceHub
from langchain.chains import RetrievalQA
import os
import csv

# Set HuggingFace API Token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Path to PDF folder
pdf_folder_path = 'E:/pycharm_project/VSproject/chatpdf/pdf4'
os.listdir(pdf_folder_path)

# Load PDF documents
loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path)]

# Create Index
index = VectorstoreIndexCreator(
    embedding=HuggingFaceEmbeddings(),
    text_splitter=CharacterTextSplitter(chunk_size=1802, chunk_overlap=0)
).from_loaders(loaders)

# Initialize LLM from HuggingFaceHub
llm = HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature":0, "max_length":512})

# Create RetrievalQA Chain
chain = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    retriever=index.vectorstore.as_retriever(),
                                    input_key="question")

# Run Query
# question = 'what kind of game does the author build?'
# question = 'what programming language is used by the author?'
# question = 'what programming language does the author use?'
# question = 'what programming language is used?'
# A text adventure game
question = 'what conclusion can you make for this book?'
# The author believes that we can indeed give any inanimate machine a soul through continuous modification and expansion of Python programs
answer = chain.run(question)

print(answer)

