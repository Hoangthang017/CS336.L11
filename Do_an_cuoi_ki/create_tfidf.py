{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "create_tfidf.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Hoangthang017/CS336.L11/blob/master/Do_an_cuoi_ki/create_tfidf.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "6kq5j1lY1cAp"
      },
      "source": [
        "# mount gg drive và clone github\r\n",
        "!git clone https://github.com/Hoangthang017/CS336.L11.git\r\n",
        "!pip install underthesea"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "96HPArVu140K"
      },
      "source": [
        "# import các thư viện cần thiết\r\n",
        "from glob import glob\r\n",
        "import os\r\n",
        "import sys\r\n",
        "from underthesea import word_tokenize\r\n",
        "import pandas as pd\r\n",
        "import numpy as np\r\n",
        "import sklearn\r\n",
        "import re\r\n",
        "import string\r\n",
        "from sklearn.feature_extraction.text import TfidfVectorizer\r\n",
        "import pickle"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "JbH6oYQJ4TWJ"
      },
      "source": [
        "# hàm tiền xử lí văn bản\r\n",
        "def text_preprocess(document):\r\n",
        "  # loại bỏ html nếu có\r\n",
        "  document_test = re.sub(r'@\\w+', '', document)\r\n",
        "\r\n",
        "  # viết thường tất cả \r\n",
        "  document_test = document_test.lower()\r\n",
        "\r\n",
        "  # bỏ dấu câu \r\n",
        "  document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)\r\n",
        "\r\n",
        "  # thay tern v_league\r\n",
        "  document_test = word_tokenize(document_test,\"text\").replace(\"v league\",\"v_league\")\r\n",
        "  \r\n",
        "  # xóa bỏ các khoảng trắng thừa \r\n",
        "  document_test = re.sub(r'\\s{2,}', ' ', document_test)\r\n",
        "\r\n",
        "  return document_test"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "vLd2LCsK2PN3"
      },
      "source": [
        "# load dataset\r\n",
        "def load_dataset(files_path):\r\n",
        "  documents_clean = []\r\n",
        "  files_name = []\r\n",
        "  # i = 0\r\n",
        "  for file_path in files_path:\r\n",
        "    # lấy tiêu đề bài viết\r\n",
        "    files_name.append(os.path.basename(file_path).replace(\".txt\",\"\"))\r\n",
        "\r\n",
        "    # lấy nội dung bài viết\r\n",
        "    content = open(file_path,encoding=\"utf8\").read()\r\n",
        "\r\n",
        "    # tiền xử lí dữ liệu\r\n",
        "    document_clean = text_preprocess(content)\r\n",
        "\r\n",
        "    # đếm số văn bản đã được load\r\n",
        "    # i += 1\r\n",
        "    # print(i)\r\n",
        "\r\n",
        "    # thêm văn bản đã load vào\r\n",
        "    documents_clean.append(document_clean)\r\n",
        "  return documents_clean, files_name;"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "U1YBjlUD8pqo"
      },
      "source": [
        "def create_tfidf(documents_clean):\r\n",
        "  # khởi tạo TfidfVectorizer\r\n",
        "  vectorizer = TfidfVectorizer()\r\n",
        "\r\n",
        "  # fit data vào TfidfVectorizer\r\n",
        "  X = vectorizer.fit_transform(documents_clean)\r\n",
        "\r\n",
        "  # chuyển vị ma trận tfidf\r\n",
        "  X = X.T.toarray()\r\n",
        "\r\n",
        "  # tạo dataframe\r\n",
        "  df_tfidf = pd.DataFrame(X, index=vectorizer.get_feature_names())\r\n",
        "\r\n",
        "  print(vectorizer)\r\n",
        "\r\n",
        "  return df_tfidf, vectorizer"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "0yY2LTj1EgMO"
      },
      "source": [
        "def get_similar_articles(q, df, files_path, vectorizer):\r\n",
        "  print(\"Câu truy vấn:\", q)\r\n",
        "  # tiền xử lí câu truy vấn\r\n",
        "  q = [text_preprocess(q)]\r\n",
        "  q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)\r\n",
        "  # print(q_vec)\r\n",
        "\r\n",
        "  sim = {}\r\n",
        "  # tính toán độ tương đồng\r\n",
        "  for i in range(len(documents_clean)):\r\n",
        "    sim[i] = np.dot(df.loc[:, str(i)].values, q_vec) / np.linalg.norm(df.loc[:, str(i)]) * np.linalg.norm(q_vec)\r\n",
        "  # print('độ dài ', len(sim))\r\n",
        "\r\n",
        "  # sắp xếp độ tương đồng\r\n",
        "  sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)\r\n",
        "  # print(type(sim_sorted))\r\n",
        "\r\n",
        "  # số lượng bài viết tìm được\r\n",
        "  rank = 10\r\n",
        "  now = 0\r\n",
        "\r\n",
        "  # in kết quả truy vấn được\r\n",
        "  for k, v in sim_sorted:\r\n",
        "    print(\"Độ tương đồng: \", v)\r\n",
        "    print(\"Tiêu đề: \", files_name[k])\r\n",
        "    print(files_path[k])\r\n",
        "    now += 1\r\n",
        "    if (now == rank):\r\n",
        "      break"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "f_CKWB9-tPRo"
      },
      "source": [
        "# unzip data\r\n",
        "import zipfile\r\n",
        "with zipfile.ZipFile(\"/content/CS336.L11/Dataset_Football/bong_da_v1.zip\", 'r') as zip_ref:\r\n",
        "    zip_ref.extractall(\"/content/CS336.L11/Do_an_cuoi_ki/dataset_football/\")\r\n",
        "# load dataset\r\n",
        "files_path = glob(\"/content/CS336.L11/Do_an_cuoi_ki/dataset_football/Bong Da/*/*.txt\")"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "44scMlZrm5cw"
      },
      "source": [
        "# load dataset\r\n",
        "documents_clean , files_name = load_dataset(files_path)\r\n",
        "# tính tfidf\r\n",
        "df_tfidf, vectorizer = create_tfidf(documents_clean)"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Pp6t1yuR1ncZ"
      },
      "source": [
        "# save file tfidf\r\n",
        "df_tfidf.to_csv('/content/CS336.L11/Do_an_cuoi_ki/dataset_tfidf/tfidf_vector.csv')\r\n",
        "\r\n",
        "# save vectorizer\r\n",
        "with open('/content/CS336.L11/Do_an_cuoi_ki/dataset_tfidf/vectorizer.pk', 'wb') as f:\r\n",
        "  pickle.dump(vectorizer, f)"
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}