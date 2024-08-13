import os
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain import HuggingFaceHub
from langchain.chains import RetrievalQA

# Set your Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Path to the folder containing PDF files
pdf_folder_path = 'E:\\pycharm_project\\VSproject\\chatpdf\\pdf'

# List PDF files in the folder
pdf_files = os.listdir(pdf_folder_path)
print(f"PDF files found: {pdf_files}")

# Load PDF files
loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in pdf_files]

# Initialize the text splitter
chunk_size = 500  # Adjust this value as needed
chunk_overlap = 100
text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

# Debug: Print out the chunks for each document
all_chunks = []
for loader in loaders:
    documents = loader.load()
    chunks = text_splitter.split_documents(documents)
    print(f"Number of chunks for {loader.file_path}: {len(chunks)}")
    all_chunks.extend(chunks)

print(f"Total number of chunks: {len(all_chunks)}")

# Create the index
index = VectorstoreIndexCreator(
    embedding=HuggingFaceEmbeddings(),
    text_splitter=text_splitter
).from_loaders(loaders)

# Ensure the index has been created correctly by retrieving some sample data
retriever = index.vectorstore.as_retriever()
print(f"Retriever has been created: {retriever is not None}")

# Define the language model
llm = HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature": 0, "max_length": 512})

# Create the retrieval QA chain
chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    input_key="question"
)

# Run a test query
question = 'What did Rick have to create ?'

answer = chain.run(question)

print(f"Question: {question}")
print(f"Answer: {answer}")
