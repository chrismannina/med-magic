from flask import Flask, redirect, render_template, url_for, request
# from flask-sqlalchemy import SQLAlchemy
from datetime import datetime

from rxnorm_api import *

app = Flask(__name__)

# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:cm214023@localhost/rxnorm'


# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     def __repr__(self):
#         return f'Event: {self.description}'

#     def __init__(self, description):
#         self.description = description

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # if request.method == 'POST':
    # #    query = request.form[]
    # #    return redirect(url_for('/search/med'))
    # else:
    return render_template('search.html')

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