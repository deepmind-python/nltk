import PyPDF2
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import numpy as np
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mplcursors
import matplotlib.font_manager as fm

# 設定字型，使用支援中文的字型，如 Microsoft JhengHei
plt.rcParams['font.family'] = ['Microsoft JhengHei']  # 或者 'SimHei'，視系統而定
plt.rcParams['axes.unicode_minus'] = False  # 確保負號正常顯示

def pdf_to_embeddings(pdf_path, model_name='bert-base-chinese'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        sentence_embeddings = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            sentences = text.split('。')

            for sentence in sentences:
                if sentence.strip():
                    inputs = tokenizer(sentence.strip(), return_tensors='pt')
                    outputs = model(**inputs)
                    embeddings = outputs.last_hidden_state.mean(dim=1)
                    sentence_embeddings.append((sentence.strip(), embeddings))

    return sentence_embeddings

def calculate_distances(query, sentence_embeddings, model_name='bert-base-chinese'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    query_inputs = tokenizer(query, return_tensors='pt')
    query_outputs = model(**query_inputs)
    query_embedding = query_outputs.last_hidden_state.mean(dim=1)

    distances = []
    for sentence, embedding in sentence_embeddings:
        distance = F.pairwise_distance(query_embedding, embedding).item()
        distances.append((sentence, embedding, distance))

    return query_embedding, distances

def plot_embeddings_3d_mds(query_sentence, query_embedding, sentence_embeddings):
    embeddings = [embedding for _, embedding, _ in sentence_embeddings]
    all_embeddings = torch.vstack(embeddings).detach().numpy()
    all_embeddings_with_query = np.vstack((all_embeddings, query_embedding.detach().numpy()))

    mds = MDS(n_components=3, dissimilarity='euclidean', random_state=42)
    reduced_embeddings_with_query = mds.fit_transform(all_embeddings_with_query)

    reduced_embeddings = reduced_embeddings_with_query[:-1]
    query_position = reduced_embeddings_with_query[-1]

    closest_sentence, _, _ = min(sentence_embeddings, key=lambda x: F.pairwise_distance(query_embedding, x[1]).item())
    closest_index = next(i for i, (sentence, _, _) in enumerate(sentence_embeddings) if sentence == closest_sentence)

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    sentence_points = []
    for i, (sentence, _, _) in enumerate(sentence_embeddings):
        x, y, z = reduced_embeddings[i]
        color = 'red' if i == closest_index else 'green'
        point = ax.plot([x], [y], [z], 'o', color=color, markersize=10)[0]
        sentence_points.append(point)

    query_point = ax.plot([query_position[0]], [query_position[1]], [query_position[2]], 'o', color='blue', markersize=15)[0]

    ax.set_title("Query and Sentence Embeddings Visualization (3D) with MDS")
    ax.set_xlabel("MDS Component 1")
    ax.set_ylabel("MDS Component 2")
    ax.set_zlabel("MDS Component 3")

    # Connect cursor with annotations
    cursor = mplcursors.cursor(sentence_points + [query_point], hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"{query_sentence}" if sel.artist == query_point else f"{sentence_embeddings[sentence_points.index(sel.artist)][0]}"
    ))

    # Hide the default box
    cursor.connect("add", lambda sel: sel.annotation.get_bbox_patch().set_alpha(0))

    plt.show()

def plot_embeddings_2d_mds(query_sentence, query_embedding, sentence_embeddings):
    embeddings = [embedding for _, embedding, _ in sentence_embeddings]
    all_embeddings = torch.vstack(embeddings).detach().numpy()
    all_embeddings_with_query = np.vstack((all_embeddings, query_embedding.detach().numpy()))

    mds = MDS(n_components=2, dissimilarity='euclidean', random_state=42)
    reduced_embeddings_with_query = mds.fit_transform(all_embeddings_with_query)

    reduced_embeddings = reduced_embeddings_with_query[:-1]
    query_position = reduced_embeddings_with_query[-1]

    closest_sentence, _, _ = min(sentence_embeddings, key=lambda x: F.pairwise_distance(query_embedding, x[1]).item())
    closest_index = next(i for i, (sentence, _, _) in enumerate(sentence_embeddings) if sentence == closest_sentence)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    sentence_points = []
    for i, (sentence, _, _) in enumerate(sentence_embeddings):
        x, y = reduced_embeddings[i]
        color = 'red' if i == closest_index else 'green'
        point = ax.plot(x, y, 'o', color=color, markersize=10)[0]
        sentence_points.append(point)

    query_point = ax.plot(query_position[0], query_position[1], 'o', color='blue', markersize=15)[0]

    ax.set_title("Query and Sentence Embeddings Visualization (2D) with MDS")
    ax.set_xlabel("MDS Component 1")
    ax.set_ylabel("MDS Component 2")

    # Connect cursor with annotations
    cursor = mplcursors.cursor(sentence_points + [query_point], hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"{query_sentence}" if sel.artist == query_point else f"{sentence_embeddings[sentence_points.index(sel.artist)][0]}"
    ))

    # Hide the default box
    cursor.connect("add", lambda sel: sel.annotation.get_bbox_patch().set_alpha(0))

    plt.show()

# Example usage
pdf_path = "preface_ct.pdf"
query = "什麼會造成網癮？"

sentence_embeddings = pdf_to_embeddings(pdf_path)
query_embedding, distances = calculate_distances(query, sentence_embeddings)

print(f"Query: {query}\n")
for sentence, _, distance in distances:
    print(f"Sentence: {sentence}")
    print(f"Distance: {distance}\n")

closest_sentence, _, closest_distance = min(distances, key=lambda x: x[2])
print(f"Closest sentence: {closest_sentence} (closest)\nDistance: {closest_distance}\n")

plot_embeddings_2d_mds(query, query_embedding, distances)
plot_embeddings_3d_mds(query, query_embedding, distances)
