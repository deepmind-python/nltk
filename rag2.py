import time
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain import HuggingFaceHub
from langchain.chains import RetrievalQA
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import textwrap

# Set up the Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Load the PDFs and create the index
pdf_folder_path = 'E:\\pycharm_project\\VSproject\\chatpdf\\pdf'
os.listdir(pdf_folder_path)

loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path)]

index = VectorstoreIndexCreator(
    embedding=HuggingFaceEmbeddings(),
    text_splitter=CharacterTextSplitter(chunk_size=1802, chunk_overlap=0)
).from_loaders(loaders)

llm = HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature": 0, "max_length": 512})

chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=index.vectorstore.as_retriever(),
    input_key="question"
)

# Ask a question and get the output
o = chain.run('Why did John have to make a cake?')

# Load images (make sure you have image files in your directory)
image_paths = ['C:/code/1.png', 'C:/code/2.png']
images = [Image.open(image_path) for image_path in image_paths]

# Load a bold font
# Adjust the font path and size as needed; this example uses Arial Bold
font_path = "C:/Windows/Fonts/arialbd.ttf"  # Path to a bold font file
font_size = 8
font = ImageFont.truetype(font_path, font_size)

# Set up the text wrapping
max_width = min(image.width for image in images) - 20  # Adjust based on smallest image size

# Wrap the text
wrapped_text = textwrap.fill(o, width=10)  # Adjust the width to fit your image

# Draw text on each image
for image in images:
    draw = ImageDraw.Draw(image)
    text_position = (80, 1)
    draw.text(text_position, wrapped_text, fill=(255,255,0), font=font)

# Loop to display the images alternately
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots(figsize=(5, 5))

while True:
    for i, image in enumerate(images):
        ax.clear()  # Clear the current image
        ax.imshow(image)
        ax.axis('off')
        plt.title(f"Image {i+1}")
        plt.draw()
        plt.pause(1)  # Display each image for 1 second
