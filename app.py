from flask import Flask,render_template,request,redirect,url_for
import random
import requests
import json
import os
app=Flask(__name__)
import Algorithmia
import flickr
from flickrapi import FlickrAPI
import urllib2
apiKey = "simJyJaH8sR1EEq+6EqwRfLtquW1"
client=Algorithmia.client(apiKey)
FLICKR_PUBLIC = 'cec2c29a56c689b48ab04e59680e152d'
FLICKR_SECRET = 'b3ae1b59e093ec86'

@app.route('/',methods=['GET','POST'])
def summarizeCode():
    if request.method=='POST':
        input=request.form['text']
        algo=client.algo('nlp/Summarizer/0.1.3')
        alg=client.algo('nlp/AutoTag/1.0.1')
        al=client.algo('nlp/SentimentAnalysis/1.0.3')
        summ=algo.pipe(request.form['text']).result
        tag=alg.pipe(request.form['text']).result
        tags=[stag.encode('utf-8') for stag in tag]
        sent=al.pipe(request.form['text']).result
        senti=sent*20
        if senti==20:
            sen="This text is very weak."
        elif senti==40:
            sen="This text is weak."
        elif senti==60:
            sen="This text is neutral."
        elif senti==80:
            sen="This text is strong."
        else:
            sen="This text is very strong."
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
    		'&image_type=photo&per_page=4&image_type=photo&'
    	)
        pixabay_response2 = requests.get(
    		'http://pixabay.com/api/?username='
    		+username+
    		'&key='
    		+key+
    		'&search_term='
    		+second+
    		'&image_type=photo&per_page=4&image_type=photo&'
    	)
        pixabay_response3 = requests.get(
    		'http://pixabay.com/api/?username='
    		+username+
    		'&key='
    		+key+
    		'&search_term='
    		+third+
    		'&image_type=photo&per_page=4&image_type=photo&'
    	)
        pixabay_response1 = pixabay_response1.json()
        pixabay_response2 = pixabay_response2.json()
        pixabay_response3 = pixabay_response3.json()
        images1 = []
        images2 = []
        images3 = []
    	for item in pixabay_response1['hits']:
    		images1.append({'preview':item['previewURL'], 'full_size':item['webformatURL']})
        for item in pixabay_response2['hits']:
    		images2.append({'preview':item['previewURL'], 'full_size':item['webformatURL']})
        for item in pixabay_response3['hits']:
    		images3.append({'preview':item['previewURL'], 'full_size':item['webformatURL']})
        #flickr image search
        flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
        extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
        #first tag
        query= flickr.photos.search(text=first, per_page=3, extras=extras)
        photos = query['photos']
        pho= photos['photo']
        p=pho[0]
        q=pho[1]
        r=pho[2]
        url1=p['url_o']
        url2=q['url_o']
        u1=url1.encode('utf-8')
        u2=url2.encode('utf-8')
        print photos
        #first tag
        #second tag
        que= flickr.photos.search(text=second, per_page=3, extras=extras)
        frame = que['photos']
        phot= frame['photo']
        s=phot[0]
        t=phot[1]
        u=phot[2]
        url4=s['url_o']
        url5=t['url_o']
        u4=url4.encode('utf-8')
        u5=url5.encode('utf-8')
        print frame
        #second tag
        #third tag
        quet= flickr.photos.search(text=third, per_page=3, extras=extras)
        snap = quet['photos']
        phor= snap['photo']
        v=phor[0]
        w=phor[1]
        x=phor[2]
        url7=v['url_o']
        url8=w['url_o']
        u7=url7.encode('utf-8')
        u8=url8.encode('utf-8')
        print snap
        #third tag
        return render_template('Summaryfinal.html',summ=summ,input=input,senti=senti,u1=u1,u2=u2,u4=u4,u5=u5,u7=u7,u8=u8,images1=images1,images2=images2,images3=images3,sen=sen,tags=tags)
    else:
        return render_template('summarizerform.html')

if __name__=='__main__':
    port=int(os.environ.get("PORT",5000))
    app.run(debug=True,host='0.0.0.0',port=port)
