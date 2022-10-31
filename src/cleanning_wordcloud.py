# scrapingからきたテキストデータをwordCloudできるよう整理する。
import pandas as pd
import MeCab
import re
from wordcloud import WordCloud

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
    print("Mecabがトリガーされた")
    # print(words)

    words_arr = []
    for i in words:
        if i == 'EOS' or i == '':
            continue

        # print(i.split("\t"))
        word_tmp = i.split("\t")[0]   # 単語
        # print(word_tmp)

        part = i.split("\t")[4].split("-")[0]  # 品詞
        # print(part)
        if not (part in parts):  # 品詞の判定
            continue
        if word_tmp in stop_words:  # stop words
            continue
        # print(word_tmp)
        words_arr.append(word_tmp)
    # print(words_arr)
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
    fontpath = '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'       # ***************fontpath***************
    wordcloud_content = WordCloud(background_color="white",
                        font_path=fontpath,
                        width=900,
                        height=500,
                        #mask=msk,
                        contour_width=1,
                        contour_color="black" 
                        ).generate(str_text)
    wordcloud_content.to_file("wc_image_ja.png")
