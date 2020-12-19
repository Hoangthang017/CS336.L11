# -*- coding: utf-8 -*-
"""create_tfidf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/Hoangthang017/CS336.L11/blob/master/Do_an_cuoi_ki/create_tfidf.ipynb
"""

# mount gg drive và clone github
!git clone https://github.com/Hoangthang017/CS336.L11.git
!pip install underthesea

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

    # đếm số văn bản đã được load
    # i += 1
    # print(i)

    # thêm văn bản đã load vào
    documents_clean.append(document_clean)
  return documents_clean, files_name;

def create_tfidf(documents_clean):
  # khởi tạo TfidfVectorizer
  vectorizer = TfidfVectorizer()

  # fit data vào TfidfVectorizer
  X = vectorizer.fit_transform(documents_clean)

  # chuyển vị ma trận tfidf
  X = X.T.toarray()

  # tạo dataframe
  df_tfidf = pd.DataFrame(X, index=vectorizer.get_feature_names())

  print(vectorizer)

  return df_tfidf, vectorizer

def get_similar_articles(q, df, files_path, vectorizer):
  print("Câu truy vấn:", q)
  # tiền xử lí câu truy vấn
  q = [text_preprocess(q)]
  q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
  # print(q_vec)

  sim = {}
  # tính toán độ tương đồng
  for i in range(len(documents_clean)):
    sim[i] = np.dot(df.loc[:, str(i)].values, q_vec) / np.linalg.norm(df.loc[:, str(i)]) * np.linalg.norm(q_vec)
  # print('độ dài ', len(sim))

  # sắp xếp độ tương đồng
  sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
  # print(type(sim_sorted))

  # số lượng bài viết tìm được
  rank = 10
  now = 0

  # in kết quả truy vấn được
  for k, v in sim_sorted:
    print("Độ tương đồng: ", v)
    print("Tiêu đề: ", files_name[k])
    print(files_path[k])
    now += 1
    if (now == rank):
      break

# unzip data
import zipfile
with zipfile.ZipFile("/content/CS336.L11/Dataset_Football/bong_da_v1.zip", 'r') as zip_ref:
    zip_ref.extractall("/content/CS336.L11/Do_an_cuoi_ki/dataset_football/")
# load dataset
files_path = glob("/content/CS336.L11/Do_an_cuoi_ki/dataset_football/Bong Da/*/*.txt")

# load dataset
documents_clean , files_name = load_dataset(files_path)
# tính tfidf
df_tfidf, vectorizer = create_tfidf(documents_clean)

# save file tfidf
df_tfidf.to_csv('/content/CS336.L11/Do_an_cuoi_ki/dataset_tfidf/tfidf_vector.csv')

# save vectorizer
with open('/content/CS336.L11/Do_an_cuoi_ki/dataset_tfidf/vectorizer.pk', 'wb') as f:
  pickle.dump(vectorizer, f)