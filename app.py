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
from flickrapi import FlickrAPI
import flickr
from flask import Flask,render_template,url_for,request,redirect
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
apiKey = "simJyJaH8sR1EEq+6EqwRfLtquW1"
client=Algorithmia.client(apiKey)
FLICKR_PUBLIC = 'cec2c29a56c689b48ab04e59680e152d'
FLICKR_SECRET = 'b3ae1b59e093ec86'


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
        #pixabay image search
        pixabay = {
            'username':'Nanikamal',
            'key':'4770023-279e0ea8fa77c59e0bd5e2486'
        }
        username='Nanikamal'
        key='4770023-279e0ea8fa77c59e0bd5e2486'
        first=tags[0]
        second=tags[1]
        third=tags[2]
        page=1
        pixabay_response1 = requests.get(
    		'http://pixabay.com/api/?username='
    		+username+
    		'&key='
    		+key+
    		'&search_term='
    		+first+
    		'&image_type=photo&per_page=3&image_type=photo&'
    	)
        pixabay_response2 = requests.get(
    		'http://pixabay.com/api/?username='
    		+username+
    		'&key='
    		+key+
    		'&search_term='
    		+second+
    		'&image_type=photo&per_page=3&image_type=photo&'
    	)
        pixabay_response3 = requests.get(
    		'http://pixabay.com/api/?username='
    		+username+
    		'&key='
    		+key+
    		'&search_term='
    		+third+
    		'&image_type=photo&per_page=3&image_type=photo&'
    	)
        pixabay_response1 = pixabay_response1.json()
        pixabay_response2 = pixabay_response2.json()
        pixabay_response3 = pixabay_response3.json()
        images1 = []
        images2 = []
        images3 = []
    	for item in pixabay_response1['hits']:
            url=item['webformatURL'].split('_')[0]
            res="_960.jpg"
            url=url+res
            images1.append({'preview':item['previewURL'], 'full_size':url,'mid':item['webformatURL']})
        for item in pixabay_response2['hits']:
            url=item['webformatURL'].split('_')[0]
            res="_960.jpg"
            url=url+res
            images2.append({'preview':item['previewURL'], 'full_size':url,'mid':item['webformatURL']})
        for item in pixabay_response3['hits']:
            url=item['webformatURL'].split('_')[0]
            res="_960.jpg"
            url=url+res
            images3.append({'preview':item['previewURL'], 'full_size':url,'mid':item['webformatURL']})
        return render_template('Summaryfinal.html',summ=summ,input=input,entry=entry,senti=senti,sen=sen,images1=images1,images2=images2,images3=images3,tags=tags)
    else:
        return render_template('summarizerform.html')


if __name__=='__main__':
    port=int(os.environ.get("PORT",5000))
    app.run(debug=True,host='0.0.0.0',port=port)
