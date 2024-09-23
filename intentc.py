import spacy
from spacy.training import Example

# 設定空白模型
nlp = spacy.blank('en')

# 新增文本分類器
text_cat = nlp.add_pipe('textcat')

# 假設我們有以下幾個外星人意圖
text_cat.add_label('peace_treaty')  # 和平條約
text_cat.add_label('attack')        # 進攻
text_cat.add_label('trade')         # 貿易
text_cat.add_label('exploration')   # 探索

# 準備訓練數據，這是外星人發送的訊息及其對應的意圖
training_data = [
    ("We come in peace to sign a treaty", {'cats': {'peace_treaty': 1, 'attack': 0, 'trade': 0, 'exploration': 0}}),
    ("Prepare for war, we will attack", {'cats': {'peace_treaty': 0, 'attack': 1, 'trade': 0, 'exploration': 0}}),
    ("We are here to exchange goods", {'cats': {'peace_treaty': 0, 'attack': 0, 'trade': 1, 'exploration': 0}}),
    ("We are explorers seeking knowledge", {'cats': {'peace_treaty': 0, 'attack': 0, 'trade': 0, 'exploration': 1}}),
]

# 訓練模型
optimizer = nlp.begin_training()
for epoch in range(10):  # 訓練10個回合
    for text, annotations in training_data:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], sgd=optimizer)

# 測試模型
def predict_intent(text):
    doc = nlp(text)
    return doc.cats

# 測試範例
# alien_message = "We are peaceful and want to sign a treaty"
alien_message = "We are prepared for food we want."
intent = predict_intent(alien_message)
print(f"Alien message: '{alien_message}'")
print("Predicted Intent:", intent)
