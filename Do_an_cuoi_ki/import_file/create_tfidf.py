
# import các thư viện cần thiết
from glob import glob
import os
import sys
from underthesea import word_tokenize
import pandas as pd
import numpy as np
import sklearn
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# hàm tiền xử lí văn bản
def text_preprocess(document):
  # loại bỏ html nếu có
  document_test = re.sub(r'@\w+', '', document)
  # viết thường tất cả 
  document_test = document_test.lower()
  # bỏ dấu câu 
  document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
  # thay tern v_league
  document_test = word_tokenize(document_test,"text").replace("v league","v_league")
  # xóa bỏ các khoảng trắng thừa 
  document_test = re.sub(r'\s{2,}', ' ', document_test)
  return document_test

# load dataset
def load_dataset(files_path):
  documents_clean = []
  files_name = []
  # i = 0
  for file_path in files_path:
    # lấy tiêu đề bài viết
    files_name.append(os.path.basename(file_path).replace(".txt",""))
    # lấy nội dung bài viết
    content = open(file_path,encoding="utf8").read()
    # tiền xử lí dữ liệu
    document_clean = text_preprocess(content)
    # thêm văn bản đã load vào
    documents_clean.append(document_clean)
  return documents_clean, files_name

def create_tfidf(documents_clean):
  # khởi tạo TfidfVectorizer
  vectorizer = TfidfVectorizer()
  # fit data vào TfidfVectorizer
  X = vectorizer.fit_transform(documents_clean)
  # chuyển vị ma trận tfidf
  X = X.T.toarray()
  # tạo dataframe
  df_tfidf = pd.DataFrame(X, index=vectorizer.get_feature_names())
  return df_tfidf, vectorizer

def get_similar_articles(q, df, vectorizer):
  # tiền xử lí câu truy vấn
  q = [q]
  q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
  # print(q_vec)
  sim = {}
  # tính toán độ tương đồng
  for i in range(df.shape[1]):
    sim[i] = np.dot(df.loc[:, str(i)].values, q_vec) / np.linalg.norm(df.loc[:, str(i)]) * np.linalg.norm(q_vec)
  # print('độ dài ', len(sim))
  # sắp xếp độ tương đồng
  sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
  # print(type(sim_sorted))
  return sim_sorted