import numpy as np
import pandas as pd
import string
import re
from YT_Transcript_Crawl import transcript_crawl
import text_cleaning
#import cluster
import visualization
import json
from flask import Flask,request,jsonify
from flask_cors import CORS
import os
import pymysql
import time

app=Flask(__name__)
CORS(app)

def show_db(data_base,table_name):
    # Access DB
    db = pymysql.connect(host='localhost', user='root', password='0801', port=3306, db=data_base)
    sql_select_Query = "select * from " + table_name
    cursor = db.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    db.close()
    col_name = [des[0] for des in cursor.description]
    
    df = pd.DataFrame(data)
    df.columns = col_name
    #print("Total number of rows in table: ", cursor.rowcount)
    return df


@app.route('/yt_viewer',methods=['POST'])
def postInput():
    insertValues = request.get_json()
    keyword = insertValues['keyword']
    user_name = insertValues['name']
    password = insertValues['password']
    print(user_name,password)
    # Audience DB
    audience_db = show_db('audience','info')
    print(audience_db)
    if(user_name in list(audience_db['name'])):
        this_user_data = audience_db[audience_db['name'] == user_name].reset_index(drop=True)
        if(this_user_data['password'][0] == password):
            YOUTUBE_API_KEY = "AIzaSyDTknTFDZbn-AhdCDZ7leKU7EGs9EHL8vA"
            
            df = transcript_crawl(keyword,YOUTUBE_API_KEY)
            transcript_data = df[df['transcript']!=''].reset_index(drop=True)

            transcript_data.rename(columns = {'transcript':'comment'}, inplace = True)
            tfidf_dataframe = text_cleaning.doc_clean(transcript_data)

            selected_words_data = text_cleaning.select_pos_neg_word(tfidf_dataframe)
            file_name = './'+keyword+"/top10_words"
            visualization.bar_chart(transcript_data,file_name)

            file_name = './'+keyword+"/all_wordcloud"+"(num_"+str(len(transcript_data))+")"
            visualization.word_cloud(transcript_data,file_name)

            # 單一分析所有doc
            for i in range(len(transcript_data)):
                title = transcript_data['title'][i]
                # 把奇怪字串移除
                exclude = set(string.punctuation)
                file = ''.join(ch for ch in title if ch not in exclude)
                #字串最後可能會是space
                if(file[-1] == ' '):
                    file = file[:-1]
                os.makedirs('./'+ keyword+'/'+file)
                word_list = transcript_data['words'][i]
                loc = './'+ keyword+'/'+file
                file_name = loc+'/wordcloud'
                visualization.word_cloud_one_doc(word_list,file_name)
                file_name = loc+'/barchart'
                visualization.bar_chart_one_doc(word_list,file_name)

            return jsonify({'num_video':len(df),'num_transcript':len(transcript_data)})
        else:
            return jsonify({'Error':'Wrong PassWord'})

    else:
        return jsonify({'Error':'Unvalid Name'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000,debug=True, use_reloader=False)



