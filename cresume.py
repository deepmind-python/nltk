import gensim
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import jieba

# 預處理文本
def preprocess(text):
    # 使用 jieba 進行中文斷詞
    words = jieba.lcut(text)
    return [word for word in words if word.strip()]

# 訓練 Word2Vec 模型
def train_word2vec(corpus):
    tokenized_corpus = [preprocess(doc) for doc in corpus]
    model = Word2Vec(sentences=tokenized_corpus, vector_size=100, window=5, min_count=1, workers=4)
    return model

# 計算文本的向量
def get_document_vector(model, doc):
    words = preprocess(doc)
    word_vectors = [model.wv[word] for word in words if word in model.wv]
    if word_vectors:
        return np.mean(word_vectors, axis=0)
    else:
        return np.zeros(model.vector_size)

# 計算簡歷和工作描述之間的相似性
def calculate_similarity(resume, job_description, model):
    resume_vector = get_document_vector(model, resume)
    job_description_vector = get_document_vector(model, job_description)
    similarity = cosine_similarity([resume_vector], [job_description_vector])
    return similarity[0][0]

# 示例文本
# resume = "經驗豐富的軟體開發人員，擁有機器學習和數據分析的專業知識。"
resume = "經驗豐富在機器手臂的研發。"
job_description = "尋找具有機器學習和資料科學經驗的軟體工程師。"

# 訓練 Word2Vec 模型
corpus = [resume, job_description]
model = train_word2vec(corpus)

# 計算相似性
relevance = calculate_similarity(resume, job_description, model)
print(f"The relevance of the resume to the job description is: {relevance:.4f}")
