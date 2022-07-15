# -*- coding: utf-8 -*-
import sys
import streamlit as st
import MeCab
import collections
from matplotlib import pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="WordCloud demo")
st.title('WordCloud demo')
if "stop" not in st.session_state:
  st.session_state["stop"] = ['街', 'なる', 'ある', '思う','いる','する','ほしい','の']

#単語の数カウント
def make_words(texts):
    m = MeCab.Tagger()
    words=[]
    for sentence in texts:
        node = m.parseToNode(sentence)
        # st.write("---")
        # st.write(sentence)
        while node:
            hinshi = node.feature.split(",")[0]
            if hinshi in ["名詞","形容詞","動詞"]:
                origin_source = node.feature.split(",")
                if len(origin_source) > 8:
                    origin = origin_source[6]
                    if origin not in st.session_state["stop"]:
                        words.append(origin)
            node = node.next
    st.write("言語処理完了")
    return(words)




#wordCloud生成
def create_wordcloud(wordlists):
    #st.write(wordlists)
    result = ' '.join(s for s in wordlists)
    st.write("クラウド作成開始")
    wc = WordCloud(
        font_path = "~/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        width=1920, 
        height=1080,
        prefer_horizontal=1,
        background_color='white',
        include_numbers=True,
        colormap='tab20',
        regexp=r"[\w']+",
    ).generate_from_text(result)
    st.write("クラウド作成完了")
    fig = plt.figure(figsize=(12,9))
    ax = plt.axes()

    st.set_option('deprecation.showPyplotGlobalUse', True)
    plt.tight_layout()
    plt.imshow(wc,interpolation="bilinear")
    plt.axis("off")
    st.pyplot(fig)
    #wc.to_file('./aaa.png')
    #st.subheader("ストップワード")
    #st.write("/".join(stop))


def main():
    texts = ["ここに解析したい文章を入れる"]
    words = ["ここ","解析","文章"]
    # 解釈するテキストの処理
    st.subheader("入力テキスト")
    text = st.text_area("注：半角英数字は無視されます", "ここに解析したいテキストを入れてください．")
    if st.button(label="解析"):
        texts=text.split("\n")
        # st.write(texts)
        words = make_words(texts)

    st.subheader("ストップワード")
    # ストップワードの処理
    add_stopword = st.text_input(label="注：半角英数字は無視されます")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(label="追加", key=2):
            if add_stopword not in st.session_state["stop"]:
                st.session_state["stop"].append(add_stopword)
    with col2:
        if st.button(label="削除", key=3): 
            if add_stopword in st.session_state["stop"]:
                st.session_state["stop"].remove(add_stopword)
    st.write("/".join(st.session_state["stop"]))  
    # 出力結果の表示
    st.subheader("出力結果")

    # 形態素解析を実施する
    words = make_words(texts)

    st.write(len(texts),len(words))
    if len(texts) != 0 and len(words) !=0:
        create_wordcloud(words)
        word_with_tf= collections.Counter(words).most_common()
    #print(c.most_common(10))
        # st.write(word_with_tf)
    else:
        st.write("no data")
    



if __name__ == "__main__":
    main()
