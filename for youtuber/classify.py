import requests
from pprint import pprint
from datetime import datetime
import numpy as np
import pandas as pd
import string
from snownlp import SnowNLP
from snownlp import sentiment
import csv
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt
import re
import emoji
import os

def pos(path):
    while True:
        global re
        result = re.match(r'^https\:\/\/www\.youtube\.com\/watch\?v\=.+$',path)
        if result:
            print('Match found: ', result.group())
            break
        else:
            print('No match')
    
    video_id = path.split('v=')[1]
    
    YOUTUBE_API_KEY = "AIzaSyDTknTFDZbn-AhdCDZ7leKU7EGs9EHL8vA"
    
    class YoutubeSpider():
        def __init__(self, api_key):
            self.base_url = "https://www.googleapis.com/youtube/v3/"
            self.api_key = api_key
    
        def get_html_to_json(self, path):
            """組合 URL 後 GET 網頁並轉換成 JSON"""
            api_url = f"{self.base_url}{path}&key={self.api_key}"
            r = requests.get(api_url)
            if r.status_code == requests.codes.ok:
                data = r.json()
            else:
                data = None
            return data
    
        def get_video(self, video_id, part='snippet,statistics'):
            """取得影片資訊"""
            # jyordOSr4cI
            # part = 'contentDetails,id,liveStreamingDetails,localizations,player,recordingDetails,snippet,statistics,status,topicDetails'
            path = f'videos?part={part}&id={video_id}'
            data = self.get_html_to_json(path)
            if not data:
                return {}
            # 以下整理並提取需要的資料
            data_item = data['items'][0]
    
            try:
                # 2019-09-29T04:17:05Z
                time_ = datetime.strptime(data_item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                # 日期格式錯誤
                time_ = None
    
            url_ = f"https://www.youtube.com/watch?v={data_item['id']}"
    
            info = {
                'id': data_item['id'],
                'channelTitle': data_item['snippet']['channelTitle'],
                'publishedAt': time_,
                'video_url': url_,
                'title': data_item['snippet']['title'],
                'description': data_item['snippet']['description'],
                'likeCount': data_item['statistics']['likeCount'],
                #'dislikeCount': data_item['statistics']['dislikeCount'],
                'commentCount': data_item['statistics']['commentCount'],
                'viewCount': data_item['statistics']['viewCount']
            }
            return info
    
        def get_comments(self, video_id, page_token='', part='snippet', max_results=100):
            """取得影片留言"""
            # jyordOSr4cI
            path = f'commentThreads?part={part}&videoId={video_id}&maxResults={max_results}&pageToken={page_token}'
            data = self.get_html_to_json(path)
            if not data:
                return [], ''
            # 下一頁的數值
            next_page_token = data.get('nextPageToken', '')
    
            # 以下整理並提取需要的資料
            comments = []
            for data_item in data['items']:
                data_item = data_item['snippet']
                top_comment = data_item['topLevelComment']
                try:
                    # 2020-08-03T16:00:56Z
                    time_ = datetime.strptime(top_comment['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    # 日期格式錯誤
                    time_ = None
    
                if 'authorChannelId' in top_comment['snippet']:
                    ru_id = top_comment['snippet']['authorChannelId']['value']
                else:
                    ru_id = ''
    
                ru_name = top_comment['snippet'].get('authorDisplayName', '')
                if not ru_name:
                    ru_name = ''
    
                comments.append({
                    'reply_id': top_comment['id'],
                    'ru_id': ru_id,
                    'ru_name': ru_name,
                    'reply_time': time_,
                    'reply_content': top_comment['snippet']['textOriginal'],
                    'rm_positive': int(top_comment['snippet']['likeCount']),
                    'rn_comment': int(data_item['totalReplyCount'])
                })
            return comments, next_page_token
    
    
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    
    video_info_dict = youtube_spider.get_video(video_id, part='snippet,statistics')
    
    
    next_page_token = ''
    comment_lists = []
    while 1:
        comments, next_page_token = youtube_spider.get_comments(video_id, page_token=next_page_token)
        comment_lists.append(comments)
        # 如果沒有下一頁留言，則跳離
        if not next_page_token:
            break
    content_list = []
    positive_list = []
    re_comment = []
    name_list = []
    comment_df = pd.DataFrame()
    
    for comment_list in comment_lists:
        for comment in comment_list:
            content_list.append(comment['reply_content'])
            positive_list.append(comment['rm_positive'])
            re_comment.append(comment['rn_comment'])
            name_list.append(comment['ru_name'])
    
    #留言儲存為dict====================================================================
    comment_df['name'] = name_list
    comment_df['comment'] = content_list
    comment_df['positive_num'] = positive_list
    comment_df['re_comment_num'] = re_comment
    comment_df = comment_df.sort_values(['positive_num'],ascending=False)
    comment_df = comment_df.reset_index(drop=True)
    
    
    #留言轉換成csv=====================================================================
    file = video_info_dict['title']
    global string
    exclude = set(string.punctuation)
    file = ''.join(ch for ch in file if ch not in exclude)
    
    new_con = []
    for i in range(0,len(content_list),1):
        a = content_list[i]
        text = emoji.demojize(a)
        result = re.sub(':\S+?:', ' ', text)
        out = result.translate(str.maketrans('', '', string.punctuation))
        characters = "’'""'!?"
        for x in range(len(characters)):
            out = out.replace(characters[x],"")
        new_con.append(out)
    
    for i in new_con:
        if ' ' in new_con:
            new_con.remove(' ')
        if '  'in new_con:
            new_con.remove('  ')
        if '   'in new_con:
            new_con.remove('   ')
        if '    'in new_con:
            new_con.remove('    ')
        if '      'in new_con:
            new_con.remove('      ')
        if '        'in new_con:
            new_con.remove('        ')
            
    for i in new_con:
        i.strip()
        if len(i) < 2:
            new_con.remove(i)
    
    ch_en = []
    for i in range(0,len(new_con)):
        #for ch in new_con[i]:
        if u'\u4e00' <= new_con[i] <= u'\u9fff':
            ch_en.append('False')
        else:
            ch_en.append('True')
        
    #以SnowNLP計算情緒指數，並分類負、中、正三種留言
    score = []
    for i in range(0,len(new_con),1):
        word = new_con[i] 
        s = SnowNLP(word)
        score.append(s.sentiments)
    
    # NLTK VADER for sentiment analysis
    from nltk.sentiment import SentimentIntensityAnalyzer
    
    columns = ['headline']
    nltk_pd = pd.DataFrame(new_con, columns=columns)
    nltk_score = []
    
    for i in range(0,len(new_con),1):
        sentence = new_con[i]
        sia = SentimentIntensityAnalyzer()
        sentiment_dict = sia.polarity_scores(sentence)        
        nltk_score.append(sentiment_dict)
            
    nltk_score_pd = pd.DataFrame(nltk_score)
    nltk_pd = pd.concat([nltk_pd, nltk_score_pd], axis=1)
    
    
    # VADER for sentiment analysis
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
     
    columns = ['headline']
    vader_pd = pd.DataFrame(new_con, columns=columns)
    vader_score = []
    
    for i in range(0,len(new_con),1):
        sentence = new_con[i]
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(sentence)        
        vader_score.append(sentiment_dict)
    
    vader_score_pd = pd.DataFrame(vader_score)
    vader_pd = pd.concat([vader_pd, vader_score_pd], axis=1)
    
    
    #Textblob
    from textblob import TextBlob
    
    score_blob =[]
    for i in range(0,len(new_con),1):
        word = new_con[i] 
        simple_text = TextBlob(word)
        score_blob.append(simple_text.sentiment.polarity)
    
    #Comparison
    columns = ['headline'] 
    
    nltk_sc = []
    for i in range(0,len(nltk_pd['compound']),1):
        nltk_sc.append(nltk_pd['compound'][i])
    
    vader_sc = []
    for i in range(0,len(vader_pd['compound']),1):
        vader_sc.append(vader_pd['compound'][i])
    
    grades = {
        "headline": new_con,
        "SnowNLP": score,
        "NLTK": nltk_sc,
        "Vader": vader_sc,
        "Textblob": score_blob
    }
     
    all_score = pd.DataFrame(grades)
    
    
    #計算各分數標準化結果
    import statistics
    st1 = statistics.pstdev(score)
    st2 = statistics.pstdev(nltk_sc)
    st3 = statistics.pstdev(vader_sc)
    st4 = statistics.pstdev(score_blob)
    mean1 = np.mean(score)
    mean2 = np.mean(nltk_sc)
    mean3 = np.mean(vader_sc)
    mean4 = np.mean(score_blob)
    
    score2 = []
    nltk_sc2 = []
    vader_sc2 = []
    score_blob2 = []
    for i in range(0,len(new_con),1):
        score2.append((score[i]-mean1)/st1)
        nltk_sc2.append((nltk_sc[i]-mean2)/st2)
        vader_sc2.append((vader_sc[i]-mean3)/st3)
        score_blob2.append((score_blob[i]-mean4)/st4)
        
    st_grades = {
        "headline": new_con,
        "SnowNLP": score2,
        "NLTK": nltk_sc2,
        "Vader": vader_sc2,
        "Textblob": score_blob2
        }
    
    st_score = pd.DataFrame(st_grades)
    
    #若全為英文或數字，由NLTK/TEXTBLOB/VADER判斷，若否，則用SNOWNLP判斷
    final_st = []
    for i in range(0,len(ch_en),1):
        if ch_en[i] == 'True':
            b = (st_grades["NLTK"][i] + st_grades["Vader"][i] + st_grades["Textblob"][i])/3
        else:
            b = st_grades["SnowNLP"][i]
        final_st.append(b)
    
    final_dict = {
        "headline": new_con,
        "final_st": final_st,
        }
    
    final_result = pd.DataFrame(final_dict)
    sentiment_score = sum(final_st)/len(final_st)
    
    
    global pos_line
    pos_line = []
    pos_score = []
    neg_line = []
    neg_score = []
    for i in range(0,len(final_result)):
        if (final_result["final_st"][i])>0:
            pos_line.append(final_result["headline"][i])
            pos_score.append(final_result["final_st"][i])
        if (final_result["final_st"][i])<0:
            neg_line.append(final_result["headline"][i])
            neg_score.append(final_result["final_st"][i])
            
    pos_dict = {
        "headline": pos_line,
        "final_st": pos_score,
        } 
    result_pos = pd.DataFrame(pos_dict)
    
    neg_dict = {
        "headline": neg_line,
        "final_st": neg_score,
        } 
    result_neg = pd.DataFrame(neg_dict)
    file = video_info_dict['title']
    exclude = set(string.punctuation)
    file = ''.join(ch for ch in file if ch not in exclude)
    file_path = './'+file
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    comment_df.to_csv(file_path+'/'+file+'.csv',index=False,encoding='utf-8-sig')
    return pos_line,file,neg_line,sentiment_score
