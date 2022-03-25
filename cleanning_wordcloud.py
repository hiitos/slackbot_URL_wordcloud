# scrapingからきたテキストデータをwordCloudできるよう整理する。
import pandas as pd
import urllib.request
from pathlib import Path
from tqdm import tqdm
import argparse
from pathlib import Path
import sys
import MeCab
import pandas as pd
import re
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np

# scrapingからくるテキストデータは,文書の連なりだと仮定
# やること
# ・分かち書き→stopword
# ・取り出すもの、とりあえず名詞、微妙なら形容詞、動詞も追加していい。
# ・単語　頻度　の２列のデータフレームをreturn

def wakati(sentence):
    # ----------------------------------
    # 記号,英数字,スペースの除外 
    code_regex = re.compile(
        '[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％©|｜0-9０-９A-Za-zＡ-Ｚａ-ｚ\s]')
    txt = sentence.rstrip()
    cleaned_text = code_regex.sub('', txt)
    #print(cleaned_text)
    # ----------------------------------

    # ***Stop Words*** # 
    # stiowords タイトル取得し、タイトルに含まれてる単語でもいい
    stop_words = ["の"]
    # ***Parts*** #
    parts = ["名詞"]
    tagger = MeCab.Tagger()
    words = tagger.parse(cleaned_text).splitlines()

    words_arr = []
    for i in words:
        if i == "EOS" or i == "":
            continue
        word_tmp = i.split()[0]   # 単語
        part = i.split()[1].split(",")[0]  # 品詞
        if not (part in parts):  # 品詞の判定
            continue
        if word_tmp in stop_words:  # stop words
            continue
        words_arr.append(word_tmp)
    #print(words_arr)
    return words_arr

def to_data(list_data):
    all_words_df = pd.DataFrame(
        {"words": list_data, "count": len(list_data)*[1]})
    words_count = all_words_df.groupby("words").sum()["count"]
    words_df = pd.DataFrame(words_count)
    words_df = words_df.loc[words_df["count"] >= 3]
    #print(words_df.sort_values("count", ascending=False))
    return words_df

def word_cloud(list_text):
    str_text = ' '.join(list_text)
    #print(str_text)
    #print(type(str_text))
    fontpath = '/Users/hitose.k/Library/Fonts/Makinas-4-Flat.otf'
    wordcloud = WordCloud(background_color="white",
                        font_path=fontpath,
                        width=900,
                        height=500,
                        #mask=msk,
                        contour_width=1,
                        contour_color="black"  # ,
                        # stopwords=set(stop_words_ja)
                          ).generate(str_text)
    wordcloud.to_file("wc_image_ja.png")

    

