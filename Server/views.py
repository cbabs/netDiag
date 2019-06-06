from Server import app

from flask import Flask, request, render_template, url_for, jsonify, redirect, flash, session
from flask_bootstrap import Bootstrap

import re
from datetime import datetime

from functools import wraps

from mongodb import MongoDb

db = MongoDb()

bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def transactions():
    
    if request.method == 'GET':
        webData = db.getAllTrans()
    
        return render_template('transactions.html', data=webData)

    if request.method == 'POST':
        
        if 'dateRange' in request.form:
            dates = request.form['dateRange']
            
            regxBegDate = r'^(.*)(\s-\s)'
            regxEndDate = '(\s-\s)(.*)'
            
            begDateRgx = re.findall(regxBegDate, dates)
            begDate = datetime.strptime(begDateRgx[0][0], '%Y-%m-%d %H:%M:%S')
            
            endDateRgx = re.findall(regxEndDate, dates)
            endDate = datetime.strptime(endDateRgx[0][1], '%Y-%m-%d %H:%M:%S')
                        
            webData = db.getTransDates(begDate, endDate)
            
            
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

    return render_template('transacs.html', data=data)
