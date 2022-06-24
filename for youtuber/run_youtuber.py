import numpy as np
import pandas as pd
import re
import classify
import text_cleaning
import visualization
import json
from flask import Flask,request,jsonify
from flask_cors import CORS
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

@app.route('/yt_youtuber',methods=['POST'])
def postInput():
    
    insertValues = request.get_json()
    path = insertValues['path']
    user_name = insertValues['name']
    password = insertValues['password']

    result = re.match(r'^https\:\/\/www\.youtube\.com\/watch\?v\=.+$',path)
    if result:
        print('Match found: ', result.group())
    else:
        print('No match')
        return jsonify({'Unsuccess':'Not A Youtube Video Link'})
    # Audience DB
    youtuber_db = show_db('youtuber','info')
    
    if(user_name in list(youtuber_db['name'])):
        this_user_data = youtuber_db[youtuber_db['name'] == user_name].reset_index(drop=True)
        if(this_user_data['password'][0] == password):

            pos_line,file,neg_line,sentiment_score = classify.pos(path)  
            #分別回傳正面留言、影片名稱、負面留言、整體分數
            tfidf_dataframe = text_cleaning.doc_clean(pos_line)

            #正面留言繪圖 
            file_name = './'+file+"/top10_words_positive"
            visualization.bar_chart(pos_line,file_name)
            file_name = './'+ file +"/all_wordcloud_positive"+"(num_"+str(len(tfidf_dataframe))+")"
            visualization.word_cloud(pos_line,file_name)

            #負面留言繪圖
            file_name = './'+file+"/top10_words_negative"
            visualization.bar_chart(neg_line,file_name)
            file_name = './'+ file +"/all_wordcloud_negative"+"(num_"+str(len(tfidf_dataframe))+")"
            visualization.word_cloud(neg_line,file_name)

            #print("所有留言的情緒指數為：",sentiment_score)
            #print("正面留言數量比例：",len(pos_line)/(len(pos_line)+len(neg_line)))
            #print("負面留言數量比例：",len(neg_line)/(len(pos_line)+len(neg_line)))
            pos_rate = len(pos_line)/(len(pos_line)+len(neg_line))

            return jsonify({'pos_rate':pos_rate})

        else:
            return jsonify({'Error':'Wrong PassWord'})
    else:
        return jsonify({'Error':'Unvalid Name'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True, use_reloader=False)



