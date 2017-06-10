from flask import Flask,render_template,request,redirect,url_for,send_file
import random
import os
import requests
import re
import cookielib
import json
app=Flask(__name__)
import Algorithmia
import urllib2
import StringIO
import traceback
import MySQLdb
from collections import Counter
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
apiKey = "simJyJaH8sR1EEq+6EqwRfLtquW1"
client=Algorithmia.client(apiKey)
db = MySQLdb.connect( host="107.178.220.200", user="aiartist", passwd="aiartist2017", db = "pixabay_links")

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        fromaddr = "mail@aiartist.io"
        toaddr = "support@aiartist.io"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = request.form['subject']

        body =request.form['msg']
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "aiartist2017")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/analyze/',methods=['GET','POST'])
def summarizeCode():
    if request.method=='POST':
        entry=request.form['text']
        input = {"to":"en","text":entry}
        algo=client.algo('nlp/Summarizer/0.1.3')
        alg=client.algo('nlp/AutoTag/1.0.1')
        al=client.algo('nlp/SentimentAnalysis/1.0.3')
        trans=client.algo('translation/YandexTranslate/0.1.2')
        data=trans.pipe(input).result
        data=[word.encode('utf-8') for word in data]
        summ=algo.pipe(data).result
        tag=alg.pipe(data).result
        tags=[stag.encode('utf-8') for stag in tag]
        sent=al.pipe(data).result
        senti=sent*20
        if senti==20:
            sen="This text is very weak"
        elif senti==40:
            sen="This text is weak"
        elif senti==60:
            sen="This text is neutral"
        elif senti==80:
            sen="This text is strong"
        else:
            sen="This text is very strong."
        first=tags[0]
        second=tags[1]
        third=tags[2]
        cursor = db.cursor()
        searchTerms = [first,second,third]
        sql_getLinks = 'SELECT pixabay_image_link FROM PIXABAY_SEARCH_QUERY WHERE tag in (%s)'
        in_p=', '.join(map(lambda x: '%s', searchTerms))
        sql_getLinks = sql_getLinks % in_p
        cursor.execute(sql_getLinks,searchTerms)
        results = cursor.fetchall()
        images = Counter(results).most_common(9)
        links=[]
        for element in images:
            link0=element[0][0].split('_')[0]
            url="_150.jpg"
            url1="_680.jpg"
            link=link0+url
            link1=link0+url1
            links.append({'pre':link,'full':link1})
        return render_template('final.html',summ=summ,input=input,entry=entry,senti=senti,sen=sen,tags=tags,links=links)
    else:
        return render_template('form.html')


if __name__=='__main__':
    port=int(os.environ.get("PORT",5000))
    app.run(debug=True,host='0.0.0.0',port=port)
