from pythainlp.tokenize import word_tokenize
from pythainlp.corpus.common import thai_stopwords
import joblib
import os

# function ที่ใช้กับ CountVectorizer
def split_text(text):
    return text.split(' ')

# load model and vectorizer
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, 'models')

MODEL_PATH = os.path.join(MODEL_DIR, 'sentiment_model.pkl')

VECTORIZE_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')

try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)

    if not os.path.exists(VECTORIZE_PATH):
        raise FileNotFoundError(f"Vectorizer file not found at {VECTORIZE_PATH}")
    vectorizer = joblib.load(VECTORIZE_PATH)

    vectorizer.analyze = lambda x:x.split(' ')
    # size of file
    # print("Vectorizer file size:", os.path.getsize(VECTORIZE_PATH))
    # print("Model file size:", os.path.getsize(MODEL_PATH))

except Exception as e:
    print(f"Error loading model or vectorizer: {e}")



thai_stopwords = list(thai_stopwords())
def text_process(text):
    text_punct = "".join(i for i in text if i not in ("?", ".", ";", ":", "!", '"', "ๆ", "ฯ"))
    text_wtk = word_tokenize(text_punct, engine="newmm")
    text_result = " ".join(i for i in text_wtk)
    text_result = " ".join(i for i in text_result.split() if i.lower not in thai_stopwords)
    return text_result

def model_pred(text):
    result_pred = None
    if isinstance(text, list):
        my_bow = vectorizer.transform(text)
    else: 
        my_bow = vectorizer.transform([text])

    result_pred = model.predict(my_bow)
    return result_pred