from Server import app

from flask import Flask, request, render_template, url_for, jsonify, redirect, flash, session
from flask_bootstrap import Bootstrap

from jinja2.ext import Extension

import re
from datetime import datetime

from functools import wraps

from mongodb import MongoDb

from rabbitMq import RabbitMq
import time

from server import NetDiag

import ast

db = MongoDb()

def is_list(value):
    return isinstance(value, list)

def is_dict(value):
    return isinstance(value, dict)

app.jinja_env.filters.update({
        'is_list': is_list,
        'is_dict': is_dict,
    })

app.jinja_env.add_extension('jinja2.ext.loopcontrols')

bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def transactions():

    if request.method == 'GET':
        webData = db.getAllTrans()

        return render_template('transactions.html', data=webData)

    if request.method == 'POST':

        if 'dateRange' in request.form:
            dates = request.form['dateRange']

            print(f"Data: {dates}")
            print(type(dates))

            regxBegDate = r'^(.*)(\s-\s)'
            regxEndDate = '(\s-\s)(.*)'

            begDateRgx = re.findall(regxBegDate, dates)
            begDate = datetime.strptime(begDateRgx[0][0], '%Y-%m-%d %H:%M:%S')

            endDateRgx = re.findall(regxEndDate, dates)
            endDate = datetime.strptime(endDateRgx[0][1], '%Y-%m-%d %H:%M:%S')

            print(f"data to getTransDates {begDate} - {endDate}")

            webData = db.getTransDates(begDate, endDate)

            print(f"From views.py: {webData}")

            return render_template('transactions.html', data=webData)

        if 'ticketNum' in request.form:
            ticketNum = request.form['ticketNum']

            webData = db.getTransTckNum(ticketNum)

            return render_template('transactions.html', data=webData)

        if 'transNum' in request.form:
            transNum = request.form['transNum']
            webData = []
            webDataDict = db.getTransac(transNum)
            webData.append(webDataDict)

            return render_template('transactions.html', data=webData)

# Get transaction by number
@app.route('/transacs/<slug>', methods=['GET'])
def transacs(slug):

    slug = int(slug)  # Convert slug into integer
    data = db.getTransac(slug)  # Get transaction by id

    print("\n\n\n")
    print(data)
    print("\n\n\n")

    return render_template('transacs.html', data=data)


# Get transaction by number
@app.route('/cmds', methods=['GET'])
def get_cmds_page():


    return render_template('cmds.html')


@app.route('/_api/upload-diag', methods=['POST'])
def deleteFilter():

    data = request.json


    NetDiag.processData(data)

    return jsonify(result=data)


@app.route('/_api/cmds', methods=['POST'])
def get_command_api():

    data = request.json

    rabMq = RabbitMq()

    replyData = rabMq.process_api_call(data)
    replyData = ast.literal_eval(replyData.decode()) 

    return jsonify(result=replyData)
