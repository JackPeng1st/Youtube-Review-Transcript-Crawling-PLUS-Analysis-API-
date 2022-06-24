from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from opencc import OpenCC
from nltk.corpus import stopwords
from nltk.tokenize import MWETokenizer
from nltk.stem import WordNetLemmatizer

def word_cloud(pos_line, file_name):
    import jieba
    from nltk.tokenize import word_tokenize
    
    words_list = []
    for i in range(0,len(pos_line),1):
        for ch in pos_line[i]:
            x = []
            #中文斷詞
            if u'\u4e00' <= ch <= u'\u9fff':
                words = jieba.cut(pos_line[i], HMM=True) 
                for word in words:
                    x.append(word)
            #英文斷詞
            else:
                text = pos_line[i]
                tokens = word_tokenize(text)
                x.extend(tokens)
        words_list.extend(x)
    cc = OpenCC('s2t')
    bg_stopwords_path="chinese_stopwords.txt"
    bg_stopwords = [cc.convert(line.strip()) for line in open(bg_stopwords_path, 'r', encoding='utf-8').readlines()]
    
    stopwords_list = ['\n','「','」',' ']
    bg_stopwords += stopwords_list  
    words_list = [char for char in words_list if char not in bg_stopwords] 
    def preprocess(words_list):
        mw_tokenizer = MWETokenizer()
        hd_list = []
        for word in words_list:
            tokens = word_tokenize(word)
            tokens=[token.lower() for token in tokens if token.isalpha()]
            hd_list += tokens

        '''# Stemming
        ps = PorterStemmer()
        #stemming an tokenize word list
        hd_politics = [ps.stem(word) for word in hd_politics]'''

        # Lemmatization
        wnl = WordNetLemmatizer()
        hd_list = [wnl.lemmatize(word) for word in hd_list]

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        hd_list = [word for word in hd_list if not word in stop_words]
        return hd_list
    tokens_list = preprocess(words_list)
    
    font_path = 'TaipeiSansTCBeta-Regular.ttf' 
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
    wc1 = WordCloud(font_path,width=1600, height=800)
    wc1.generate(' '.join(tokens_list))
    #print(wc1.words_)
    wc1.to_file(file_name+".jpg")

def bar_chart(pos_line, file_name):
    import jieba
    from nltk.tokenize import word_tokenize
    
    words_list = []
    for i in range(0,len(pos_line),1):
        for ch in pos_line[i]:
            x = []
            #中文斷詞
            if u'\u4e00' <= ch <= u'\u9fff':
                words = jieba.cut(pos_line[i], HMM=True) 
                for word in words:
                    x.append(word)
            #英文斷詞
            else:
                text = pos_line[i]
                tokens = word_tokenize(text)
                x.extend(tokens)
        words_list.extend(x)
    cc = OpenCC('s2t')
    bg_stopwords_path="chinese_stopwords.txt"
    bg_stopwords = [cc.convert(line.strip()) for line in open(bg_stopwords_path, 'r', encoding='utf-8').readlines()]
    
    stopwords_list = ['\n','「','」',' ']
    bg_stopwords += stopwords_list  
    words_list = [char for char in words_list if char not in bg_stopwords] 
    def preprocess(words_list):
        mw_tokenizer = MWETokenizer()
        hd_list = []
        for word in words_list:
            tokens = word_tokenize(word)
            tokens=[token.lower() for token in tokens if token.isalpha()]
            hd_list += tokens

        '''# Stemming
        ps = PorterStemmer()
        #stemming an tokenize word list
        hd_politics = [ps.stem(word) for word in hd_politics]'''

        # Lemmatization
        wnl = WordNetLemmatizer()
        hd_list = [wnl.lemmatize(word) for word in hd_list]

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        hd_list = [word for word in hd_list if not word in stop_words]
        return hd_list
    tokens_list = preprocess(words_list)

    words_freq = pd.Series(tokens_list).value_counts()
    df = words_freq[0:10]
    plt.rcParams['font.sans-serif'] = ['Yu Gothic']  #也可以改成Taipei
    plt.figure(figsize=(30,12),dpi=100)
    plt.bar(df.index,
			df.values, 
			width=0.5, 
			bottom=None, 
			align='center', 
			)
    for index,data in enumerate(df.values):
        plt.text(x=index , y =data , s=f"{data}" , fontdict=dict(fontsize=20))
    plt.xticks(rotation=45,fontsize=15)
    plt.yticks(fontsize=15)
    title='top 10 words'
    plt.title(title,fontsize=25)
    plt.savefig(file_name+".jpg")