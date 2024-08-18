from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# Reading from the text
from langchain import HuggingFaceHub

pdf_folder_path = 'E:\\pycharm_project\\VSproject\\chatpdf\\pdf2'
os.listdir(pdf_folder_path)

loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path)]

index = VectorstoreIndexCreator(
    embedding=HuggingFaceEmbeddings(),
    text_splitter=CharacterTextSplitter(chunk_size=1802, chunk_overlap=0)).from_loaders(loaders)

llm = HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature":0, "max_length":512})

from langchain.chains import RetrievalQA
chain = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    retriever=index.vectorstore.as_retriever(),
                                    input_key="question")

# o = chain.run('Who is Jessica?')

o = chain.run('Who are we gonna to pick up?')
# o = chain.run('Why did John have to make a cake?')
# Print o and add an image of a person speaking
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# Load an image of a person (make sure you have an image file in your directory)
image_path = 'C:/code/1.png'
image = Image.open(image_path)

# Draw the text on the image
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Adjust the position and size of the text
text_position = (0, 0)  # You can change the position based on your needs
draw.text(text_position, o, (255, 255, 255), font=font)

# Display the image with the text
plt.figure(figsize=(5, 5))
plt.imshow(image)
plt.axis('off')
plt.show()
