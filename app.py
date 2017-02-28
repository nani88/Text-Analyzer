from flask import Flask,render_template,request,redirect,url_for
import random
import os 
app=Flask(__name__)
import Algorithmia
apiKey = "simJyJaH8sR1EEq+6EqwRfLtquW1"
client=Algorithmia.client(apiKey)

@app.route('/analyze/',methods=['GET','POST'])
def summarizeCode():
    if request.method=='POST':
        input=request.form['text']
        algo=client.algo('nlp/Summarizer/0.1.3')
        alg=client.algo('nlp/AutoTag/1.0.1')
        al=client.algo('nlp/SentimentAnalysis/1.0.3')
        summ=algo.pipe(request.form['text']).result
        tag=alg.pipe(request.form['text']).result
        sent=al.pipe(request.form['text']).result
        return render_template('summary.html',summ=summ,input=input,sent=sent,tag=tag)
    else:
        return render_template('summarizerform.html')

if __name__=='__main__':
    port=int(os.environ.get("PORT",5000))
    app.run(debug=True,port=port)
