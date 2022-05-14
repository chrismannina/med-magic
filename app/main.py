from flask import Flask, redirect, render_template, url_for, request
# from flask-sqlalchemy import SQLAlchemy
from datetime import datetime
import os

from api.rxnorm import *

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # post request
    if request.method == 'POST':
        sel = request.form['sel']
        query = request.form['search']
        print('sel = ', sel, ' | query = ',query)
        print(type(sel))
        if sel == 'image':
            return redirect(url_for('img_srv', query=query))
        print('redirected to search_res wiht q:', query)
        return redirect(url_for('search_res', query=query))
    # get request
    else:
        return render_template('search.html')

@app.route('/image/<query>')
def img_srv(query):
    img = {}
    img['keyword'] = query
    # r = requests.post('http://localhost:3123/image', data=img)
    r = requests.post('https://image-srv.herokuapp.com/image', data=img)
    res = r.json()
    return render_template('image.html', url=res['image'])

@app.route('/api/<query>')
def search_res(query):
    try:    
        res = rxnorm(query)
        num = str(len(res))
        r = requests.get(f'https://uuid-genie.herokuapp.com/api/uuid/{num}')
        uuid = r.json()
    except:
        # add alert here and send back to search page
        return redirect('search')
    return render_template('search-res.html', meds=res, uuid=uuid)

@app.route('/query-db', methods=['GET'])
def query_db():
    return render_template('query-db.html')

@app.route('/csv-wizard', methods=['GET'])
def csv_wizard():
    return render_template('csv-wizard.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug=True)