
# 必須用下列方式安裝下列：
# pip install --upgrade pdfminer.six
# pip install unstructured_pytesseract

# pip install pdf2image
# pip install pdfminer
# pip install opencv-python
# pip install --upgrade pdfminer.six
# pip install unstructured_pytesseract
# pip install pandas
# pip install langchain


from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator

import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"


from langchain.embeddings import HuggingFaceEmbeddings

from langchain.text_splitter import CharacterTextSplitter

### reading from the text
from langchain import HuggingFaceHub
from langchain.document_loaders import UnstructuredPDFLoader

pdf_folder_path = 'E:\pycharm_project\VSproject\chatpdf\pdf'
os.listdir(pdf_folder_path)

loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path)]

index = VectorstoreIndexCreator(
    embedding=HuggingFaceEmbeddings(),
    # text_splitter=CharacterTextSplitter(chunk_size=1139, chunk_overlap=0)).from_loaders(loaders)
    text_splitter=CharacterTextSplitter(chunk_size=1802, chunk_overlap=0)).from_loaders(loaders)

llm=HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature":1, "max_length":512})


from langchain.chains import RetrievalQA
chain = RetrievalQA.from_chain_type(llm=llm, 
                                    chain_type="stuff", 
                                    retriever=index.vectorstore.as_retriever(), 
                                    input_key="question")

# o = chain.run('Tell me his education')
# pdf3
# o = chain.run('What is GPT4All')
# pdf2
# o = chain.run('Who is Jessica?')
o = chain.run('Who are we gonna to pick up?')

# pdf
# o = chain.run('What did Rick have to create ?')
# o = chain.run('Who are we going to pick up ?')

print(o)








