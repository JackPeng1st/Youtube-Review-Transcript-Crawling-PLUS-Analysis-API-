import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import urllib
import re
from time import sleep
from datetime import datetime
import os
from youtube_transcript_api import YouTubeTranscriptApi


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

def generate_transcript(id):
    transcript = YouTubeTranscriptApi.get_transcript(id,languages=['zh-TW']) #字幕語言
    script = ""

    for text in transcript:
        t = text["text"]
        if t != '[Music]':
            script += t + " "
    return script, len(script.split())

def transcript_crawl(keyword,YOUTUBE_API_KEY):
    options = Options()
    options.add_argument("--disable-notifications")
    #keyword = input("Please Enter the Keyword：")

    os.makedirs('./'+ keyword)

    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    driver.get("https://www.youtube.com/results?search_query=" + urllib.parse.quote(keyword)+"&sp=CAM%253D")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    link_list = []
    start = 0
    to = 5000 
    for i in range(15):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            link_str = link.get('href')
            if (link_str != None):
                result = re.match(r'^\/watch\?v\=.+$',link_str)
                if result:
                    link_list.append('https://www.youtube.com'+link_str)

        # 4.滾動條操作
        # 4.1 滾動條向下滾動
        #js_down = "window.scrollTo(0,2000)"
        js_down = "window.scrollTo("+str(start)+","+str(to)+")"
        # 執行向下滾動操作
        driver.execute_script(js_down)
        sleep(0.1)
        start = start + 5000
        to = to + 5000
    driver.close()
    '''# 向下滾動操作
    # n為從頂部往下移動滾動距離
    js1 = "var q=document.documentElement.scrollTop=2000"
    driver.execute_script(js1)
    sleep(2)            '''
                

    link_list = list(pd.Series(link_list).unique())
    # 爬到影片的id
    id_list = []
    for link in link_list:
        video_id = link.split('v=')[1]
        video_id = video_id.split('=')[0]
        video_id = video_id.split('&')[0]
        id_list.append(video_id)
    id_list = list(pd.Series(id_list).unique())

    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    transcript_list = []
    info_list = []

    for video_id in id_list:
        try:
            info = youtube_spider.get_video(video_id, part='snippet,statistics')
            info_list.append(info)
            #print(video_id)
            try:
                transcript, no_of_words = generate_transcript(video_id)
                transcript_list.append(transcript)

            except:
                transcript_list.append('')
                continue
        except:
            continue
    data = pd.DataFrame(info_list)
    data['transcript'] = transcript_list
    print(len(data['transcript'].value_counts().index),len(data['transcript'].value_counts().index)/len(data))
    data.to_csv('./'+keyword+'/'+keyword+'_YT_Video_Transcript.csv',index=False, encoding='utf-8-sig')

    return data