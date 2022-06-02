from flask import Flask, redirect, render_template, url_for, request
from datetime import datetime
from flask import current_app as app
from .api import *


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # POST request
    if request.method == 'POST':
        sel = request.form['sel']
        query = request.form['search']
        if sel == 'getDrugs':
            return redirect(url_for('drugs', query=query))
        elif sel == 'getApproximateMatch':
            print('approx', query)
            return redirect(url_for('approx_match', query=query))
        elif sel == 'image':
            return redirect(url_for('img_srv', query=query))
    # GET request
    else:
        return render_template('search.html')

@app.route('/drugs/<query>')
def drugs(query):
    try:    
        res = rxnorm(query, 'getDrugs')
    except:
        return redirect('search')
    return render_template('drugs.html', meds=res)

@app.route('/approx-match/<query>')
def approx_match(query):
    try:    
        res = rxnorm(query, 'getApproximateMatch')
        r = requests.get('https://uuid-genie.herokuapp.com/api/uuid')
        uuid = r.json()
    except:
        return redirect('search')
    return render_template('approx-match.html', meds=res, uuid=uuid)

@app.route('/image/<query>')
def img_srv(query):
    img = {}
    img['keyword'] = query
    r = requests.post('https://image-srv.herokuapp.com/image', data=img)
    res = r.json()
    return render_template('image.html', url=res['image'])

@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

# @app.route('/query-db', methods=['GET'])
# def query_db():
#     return render_template('query-db.html')

# @app.route('/csv-wizard', methods=['GET'])
# def csv_wizard():
#     return render_template('csv-wizard.html')
