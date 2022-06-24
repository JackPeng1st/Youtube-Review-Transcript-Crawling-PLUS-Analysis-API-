## The source of text documents, how do you get them：
  For Youtubers: 
    Users input an URL of YouTube to crawl the comments for analysis.
  For Viewers:
	  Users input a keyword to crawl the transcripts of videos on Youtube for analysis.
 
## The sequence of processing the text：
  Combined with DataBase (just the user in database can use this API service)
  For Youtubers: 
    Crawling review of video on YouTube. 
    The user inputs the URL of the certain video he/she wants to crawl.
    We use Regular Expression to make sure the input URL matches the YouTube URL. If the link isn’t a Youtube URL, it will output a json format to show failure.
    Doing some text mining analysis 
    Tokenizing words with NLTK.
    Stemming and lemmatizing words to reduce inflectional or derivationally related forms of a word to a common base form.
    Creating a custom stopwords.txt and removing the stopwords from the tokens list. (Available in English and Chinese respectively.)
    Creating bag words and calculating TF-IDF with cosine normalization, then converting it to dataframe.
    Doing sentimental analysis by SnowNLP, NLTK, Vader, and Textblob. SnowNLP applies to  Chinese comments, and the others apply to English comments. 
    After standardizing the sentimental score, we divide the comments into “positive comments” and “negative comments”.
    Visualizing all the results.
    Visualizing a bar chart to show the top 10 keywords of the positive and negative comments.
    Visualizing one Word Cloud for the positive and negative comments.
    return ratio of positive comments (json format)
  For Viewers:
    Crawling Transcripts of video on YouTube. 
    The user inputs the keywords that he/she wants to crawl.
    After crawling, it will return a json to show the number of videos that crawled and the number of videos that have transcripts.  
    Doing some text mining analysis 
    Tokenizing words with NLTK.
    Stemming and lemmatizing words to reduce inflectional or derivationally related forms of a word to a common base form.
    Creating a custom stopwords.txt and removing the stopwords from the tokens list. (Available in English and Chinese respectively.)
    Creating bag words and calculating TF-IDF with cosine normalization, then converting it to dataframe.
    Visualizing all the results.
    Visualizing a bar chart to show the top 10 keywords of the comments.
    Visualizing one Word Cloud for the key words.
    Making crawling and analysis code be a module API.
    API testing with Postman.

