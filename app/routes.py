from flask import Flask, redirect, render_template, url_for, request, flash, Markup
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
        # "Find All Drugs" selected
        if sel == 'getDrugs':
            return redirect(url_for('drugs', query=query))
        # "Approximate Match" selected
        elif sel == 'getApproximateMatch':
            return redirect(url_for('approx_match', query=query))
        # "Image" selected
        elif sel == 'image':
            return redirect(url_for('img_srv', query=query))
        # No function was selected
        else:
            # markup marks a string as being safe for inclusion in HTML output without needing to be escaped
            flash(Markup('<strong>Please select a function.</strong> Not sure which to use? Click <a href="/help" class="alert-link">here</a> to view the help page.'))
            return render_template('search.html')
    # GET request
    else:
        return render_template('search.html')

@app.route('/drugs/<query>')
def drugs(query):
    try:
        res = rxnorm(query, 'getDrugs')
        return render_template('drugs.html', meds=res)
    except:
        return render_template('error.html')

@app.route('/approx-match/<query>')
def approx_match(query):
    try:    
        res = rxnorm(query, 'getApproximateMatch')
        return render_template('approx-match.html', meds=res)
    except:
        return render_template('error.html')
    
@app.route('/image/<query>')
def img_srv(query):
    try:
        img = {}
        img['keyword'] = query
        r = requests.post('https://image-srv.herokuapp.com/image', data=img)
        res = r.json()
        return render_template('image.html', url=res['image'])
    except:
        return render_template('error.html')

@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
