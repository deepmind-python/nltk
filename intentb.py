import spacy
from spacy import displacy
import webbrowser
import threading
# 加載英語模型
nlp = spacy.load('en_core_web_sm')

doc = nlp(u'Show me the best hotel in Taipei')

#
for token in doc:
    if token.dep_ == 'dobj':
        print(token.head.text + token.text.capitalize())

# 定義一個函數來啟動可視化伺服器
def start_server():
    displacy.serve(doc, style='dep')

# 使用線程啟動伺服器
threading.Thread(target=start_server).start()

# 開啟預設瀏覽器
webbrowser.open('http://127.0.0.1:5000')

# ---------------------------------------------------------------

