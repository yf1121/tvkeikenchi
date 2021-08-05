from flask import Flask, render_template, request, redirect
from epgtools import nowepg
import json
import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_secret = os.environ.get("ACCESS_SECRET")

timeline = {}

nowtime = datetime.datetime.now()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('goldmedalgame-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    name = request.args.get('name', '')
    password = request.args.get('pass', '')
    frompoint = request.args.get('fp', '')
    rireki = []
    sum = 0
    rank = 0
    
    if name != "":
        if password != "" and frompoint == "":
            doc_ref = db.collection(u'users').document(name)
            doc = doc_ref.get()
            if doc.exists:
                if doc.to_dict().password == password:
                    return redirect('/?name=' + name + '&fp=true')
            else:
                doc_ref.set({
                    u'password': password,
                    u'rireki': [],
                    u'time': 0,
                })
                return redirect('/?name=' + name + '&fp=true')
        elif frompoint == "true":
            doc_ref = db.collection(u'users').document(name)
            doc = doc_ref.get()
            if doc.exists:
                rireki = doc.to_dict()['rireki']
                
                for r in rireki:
                    sum += r['length']
                docall = db.collection(u'users').stream()

                if sum != doc.to_dict()['time']:
                    doc_ref.update({u'time': sum})
                
                alldata = []
                for doc in docall:
                    alldata.append(doc.to_dict()['time'])
                alldata.sort(reverse=True)
                j = 0
                rank = len(alldata)
                for d in alldata:
                    if d < sum:
                        rank = j + 1
                    j += 1

            else:
                return redirect('/')

    return render_template('tweet.html', title='てれびのけいけんち', name=name, rireki=rireki, sum=sum, rank=rank, rirekilen=len(rireki))

@app.route('/up')
def up():
    name = request.args.get('name', '')
    area = request.args.get('area', '23')
    group = request.args.get('group', '10')
    nowlist = sorted(nowepg.get(group, area), key=lambda x: x['ch'])

    return render_template('tsumu.html', title='けいけんをつむ | てれびのけいけんち', nowonair=nowlist, name=name)

@app.route('/epg')
def epg():
    name = request.args.get('name', '')
    pg = request.args.get('pg', '')
    onair = []
    if pg != '':
        onair = nowepg.detail(pg)

    date_dt = datetime.datetime.strptime(str(nowtime.year) + '/' + onair[4] + ' ' + onair[6], '%Y/%m/%d %H:%M')

    if nowtime > date_dt:
        return redirect('/up?name=' + name)

    keika = 0
    if name != '':
        users_ref = db.collection(u'users').document(name)
        docs = users_ref.get()
        if docs.exists:
            rireki = docs.to_dict()["rireki"]
            date_start = datetime.datetime.strptime(str(nowtime.year) + '/' + onair[4] + ' ' + onair[5], '%Y/%m/%d %H:%M')

            start = date_start.strftime('%Y/%m/%d %H:%M')
                
            if len(rireki) > 0:
                if rireki[len(rireki)-1]['start'] == start and rireki[len(rireki)-1]['ch'] == onair[7]:
                    keika = rireki[len(rireki)-1]['length'] + 1
                    rireki[len(rireki)-1]['length'] = keika
                else:
                    map = {}
                    map['start'] = start
                    map['ch'] = onair[7]
                    map['length'] = keika
                    map['title'] = onair[0]
                    map['summary'] = onair[1]
                    map['category'] = onair[3]
                    map['end'] = onair[6]
                    rireki.append(map)
            else:
                map = {}
                map['start'] = start
                map['ch'] = onair[7]
                map['length'] = keika
                map['title'] = onair[0]
                map['summary'] = onair[1]
                map['category'] = onair[3]
                map['end'] = onair[6]
                rireki.append(map)

            users_ref.update({u'rireki': rireki})
        else:
            name = ''

    return render_template('tsumu_detail.html', title='けいけんをつむ | てれびのけいけんち', onair=onair, name=name, keika=keika)

# ステータスエラー時
@app.errorhandler(404)
def error_404(e):
    result = {
        "result":False,
        "message":"Not Found",
        "status":404
    }
    return result

@app.errorhandler(500)
def error_500(e):
    result = {
        "result":False,
        "message":"Internal Server Error",
        "status":500
    }
    return result


## おまじない
if __name__ == "__main__":
    app.run(debug = True)