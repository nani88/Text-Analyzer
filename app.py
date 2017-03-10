from flask import Flask,render_template,request,redirect,url_for
import random
import requests
import json
import os
app=Flask(__name__)
import Algorithmia
apiKey = "simJyJaH8sR1EEq+6EqwRfLtquW1"
client=Algorithmia.client(apiKey)

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
    		images1.append({'preview':item['previewURL'], 'full_size':item['webformatURL']})
        for item in pixabay_response2['hits']:
    		images2.append({'preview':item['previewURL'], 'full_size':item['webformatURL']})
        for item in pixabay_response3['hits']:
    		images3.append({'preview':item['previewURL'], 'full_size':item['webformatURL']})
        return render_template('Summaryfinal.html',summ=summ,input=input,senti=senti,sen=sen,tags=tags)
    else:
        return render_template('summarizerform.html')

if __name__=='__main__':
    port=int(os.environ.get("PORT",5000))
    app.run(debug=True,host='0.0.0.0',port=port)
