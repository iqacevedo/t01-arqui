#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import time
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    message = StringField('message', validators=[DataRequired()])
    submit = SubmitField('Guardar mensaje')

def insert_message(ip_message, message, conn):
    """ insert a new item into the comments table """
    sql = """INSERT INTO comments(comment_ip, comment_time, comment_message)
             VALUES(%s, %s, %s);"""
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (ip_message, time.strftime('%Y-%m-%d %H:%M:%S'), message))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)



def create_app():
    app = Flask(__name__)
    return app

app = create_app()
app.config['SECRET_KEY'] = 'you-will-never-guess'
# app.config['DEBUG'] = True
# REPLACE WITH YOUR DATABASE NAME
# MONGODATABASE = "myDatabase"
# MONGOSERVER = "localhost"0
#MONGOPORT = 27017
#client = MongoClient(MONGOSERVER, MONGOPORT)
#mongodb = client[MONGODATABASE]

# Uncomment for postgres connection
# REPLACE WITH YOUR DATABASE NAME, USER AND PASS

POSTGRESDATABASE = "flaskdb"
POSTGRESUSER = "administrator"
POSTGRESPASS = "holas"
postgresdb = psycopg2.connect(
    database=POSTGRESDATABASE,
    user=POSTGRESUSER,
    password=POSTGRESPASS)

#Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = 'queries'

'''
@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.message.data))
        insert_message(request.remote_addr, form.message.data, postgresdb)
        return redirect('/comments')
    return render_template('home.html', title='Guardar mensaje', form=form)


@app.route("/comments")
def comments():
    query = "SELECT comment_ip, comment_time, comment_message FROM comments ORDER BY comment_time"
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    results.insert(0, ["IP", "Hora del mensaje", "Mensaje"])
    
    return render_template('postgres.html', results=results)


'''
@app.route("/example")
def example():
    return render_template('example.html')

@app.route("/hola", methods=["GET"])
def hola():
    return jsonify({'ip': request.remote_addr, 'time': datetime.now()}), 200

@app.route("/abc")
def abc():
    query = "SELECT comment_ip, comment_time, comment_message FROM comments ORDER BY comment_time"
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    return jsonify(results)

'''

if __name__ == "__main__":
    app.run()
