## The source of text documents：
  For Youtubers:  
    Users input an URL of YouTube to crawl the comments for analysis.
  For Viewers:  
  	Users input a keyword to crawl the transcripts of videos on Youtube for analysis.
 
## The sequence of processing the text：
  Combined with DataBase (just the user in database can use this API service)
  For Youtubers:
  
    1. Crawling review of video on YouTube.
    2. The user inputs the URL of the certain video he/she wants to crawl.
    3. We use Regular Expression to make sure the input URL matches the YouTube URL. If the link isn’t a Youtube URL, it will output a json format to show failure.
    4. Doing some text mining analysis 
    5. Tokenizing words with NLTK.
    6. Stemming and lemmatizing words to reduce inflectional or derivationally related forms of a word to a common base form.
    7. Creating a custom stopwords.txt and removing the stopwords from the tokens list. (Available in English and Chinese respectively.)
    8. Creating bag words and calculating TF-IDF with cosine normalization, then converting it to dataframe.
    9. Doing sentimental analysis by SnowNLP, NLTK, Vader, and Textblob. SnowNLP applies to  Chinese comments, and the others apply to English comments. 
    10. After standardizing the sentimental score, we divide the comments into “positive comments” and “negative comments”.
    11. Visualizing all the results.
    12. Visualizing a bar chart to show the top 10 keywords of the positive and negative comments.
    13. Visualizing one Word Cloud for the positive and negative comments.
    14. return ratio of positive comments (json format)
  For Viewers:
  
    1. Crawling Transcripts of video on YouTube. 
    2. The user inputs the keywords that he/she wants to crawl.
    3. After crawling, it will return a json to show the number of videos that crawled and the number of videos that have transcripts.  
    4. Doing some text mining analysis 
    5. Tokenizing words with NLTK.
    6. Stemming and lemmatizing words to reduce inflectional or derivationally related forms of a word to a common base form.
    7. Creating a custom stopwords.txt and removing the stopwords from the tokens list. (Available in English and Chinese respectively.)
    8. Creating bag words and calculating TF-IDF with cosine normalization, then converting it to dataframe.
    9. Visualizing all the results.
    10. Visualizing a bar chart to show the top 10 keywords of the comments.
    11. Visualizing one Word Cloud for the key words.
    12. Making crawling and analysis code be a module API.
    13. API testing with Postman.

