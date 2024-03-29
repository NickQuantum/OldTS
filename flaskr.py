# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 22:26:52 2015

@author: U23139
"""

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import json
import pprint
#import pandas as pd


# configuration
DATABASE = 'C:\\Users\\u23139\\flaskr\\tmp\\test.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


tweets_data_path = 'C://Users//u23139//flaskr//tweet_search.txt'        
tweets_data = []
tweets_file = open(tweets_data_path, "r")

for line in tweets_file:
        try:
            tweet = json.loads(line)
            #pprint.pprint(tweet["text"])
            pprint.pprint(tweet["user"]["screen_name"])
           #print tweet
            #tweet["text"]
            #tweets_data.append(tweet)
            hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
            print(hashtags)
            tweets_data.append([tweet["text"],tweet["user"]["screen_name"],
                               hashtags])
            pprint.pprint(tweets_data)
            
        except:
            continue
#create out little application 
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/showtable')
def show_table():
    #table = g.dyndb.get_table('entries')
    #entries = table.scan()
    #logging.info('show_table: N=%s' % entries)
    tweets = tweets_data
    return render_template('show_table.html', tweets=tweets)

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/search', methods=['GET', 'POST'])
def search():
     #error = None
    if request.method == 'POST':
         print "Code gets here"        
         query = request.form['Query']
         
         return query
         #return redirect(url_for('show_table'))     
    
    else:
         return render_template('search.html')
      
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(debug=True)