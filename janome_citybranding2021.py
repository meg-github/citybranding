import streamlit as st
#import MeCab
from janome.tokenizer import Tokenizer
import collections
from matplotlib import pyplot as plt
from wordcloud import WordCloud


st.set_page_config(page_title="十三プロジェクト用テキスト解析器")
st.title('十三プロジェクト用テキスト解析器')
if "stop" not in st.session_state:
  st.session_state["stop"] = ['街', 'なる', 'ある', '思う','いる','する','ほしい','の']


hinshi_list={}


#単語の数カウント
def make_words(texts):
    m = MeCab.Tagger ()
    words=[]
    for sentence in texts:
        node = m.parseToNode(sentence)
        #st.write("---")
        #st.write(sentence)
        while node:
            hinshi = node.feature.split(",")[0]
            if hinshi in ["名詞","形容詞","動詞","固有名詞"]:
                origin_source = node.feature.split(",")
                if len(origin_source) > 10:
                    origin = origin_source[10]
                    if origin not in st.session_state["stop"]:
                        words.append(origin)
            node = node.next
    st.write("言語処理完了")
    return(words)

#m = Tokenizer()
def make_words2(texts):
    m = Tokenizer(mmap=False)
    words = []
    for sentence in texts:
        node = m.tokenize(sentence)
        for a_word in node:
            hinshi = a_word.part_of_speech.split(",")[0]
            if hinshi not in hinshi_list.keys():
                hinshi_list[hinshi] = 1
            else:
                hinshi_list[hinshi] += 1
            if hinshi in ["名詞","形容詞","動詞","固有名詞"]:
                if a_word.base_form not in st.session_state["stop"]:#ストップワードの適用
                    words.append(a_word.base_form)
                #print(type(a_word))
                #print(a_word.base_form)
                #print(a_word.part_of_speech.split(",")[0])
        #st.write(words)
        #st.write("JanomeDone")
    # st.write(hinshi_list)
    return(words)



#wordCloud生成
def create_wordcloud(wordlists):
    #st.write(wordlists)
    result = ' '.join(s for s in wordlists)
    st.write("ワードクラウド作成開始")
    wc = WordCloud(
        font_path = "SourceHanSerifK-Light.otf",
        width=1920, 
        height=1080,
        prefer_horizontal=1,
        background_color='white',
        include_numbers=True,
        colormap='tab20',
        regexp=r"[\w']+",
    ).generate_from_text(result)
    st.write("ワードクラウド作成完了")
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
    texts = []#"ここに解析し文章を入れる"]
    #words = ["ここ","解析","文章"]
    # 解釈するテキストの処理
    st.subheader("入力テキスト")
    text = st.text_area("このシステムは入力された文章を解析し，文章に出現する単語を反映した画像を生成します．文章の中に多く出現する単語はより大きく，そうでない単語は小さく表示されます．"+"\n"+"ここに解析したいテキストを入れてください．")
    if st.button(label="解析"):
        texts=text.split("\n")
        #st.write(texts)
        #st.write("だべ")
        #words = make_words(texts)


    st.subheader("分析対象から除く語")
    # ストップワードの処理
    add_stopword = st.text_input(label="ここでは分析の対象から除く単語を設定することができます．「もの」や「する」など，日常でも頻繁に使われる単語を対象外にすることで，入力した文章の特徴を観察することができます．"+"\n"+"下の枠に語を設定し，「追加」ボタンを押すことで追加できます．「削除」を押すと入力された単語がリストから削除されます．")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(label="追加", key=2):
            if add_stopword not in st.session_state["stop"]:
                st.session_state["stop"].append(add_stopword)
    with col2:
        if st.button(label="削除", key=3): 
            if add_stopword in st.session_state["stop"]:
                st.session_state["stop"].remove(add_stopword)
    st.write("現在のリスト:"+"\n"+"/".join(st.session_state["stop"]))  
    # 出力結果の表示
    #st.subheader("出力結果")


    # 形態素解析を実施する
    words = make_words2(texts)
    #st.write(words)
    #st.write("-done-")


    #st.write(len(texts),len(words))

 
    if len(texts) != 0 and len(words) !=0:
        st.subheader("ワードクラウド")
        create_wordcloud(words)
        word_with_tf= collections.Counter(words).most_common()
    #print(c.most_common(10))
        st.subheader("出現単語頻度")
        st.table(word_with_tf)
    else:
        st.write("データが入力されていません")

if __name__ == "__main__":
    main()

