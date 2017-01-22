"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from Rendezvous import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='If you have any issues while using Rendezvous With Me - contact us at:'
    )

@app.route('/plan')
def plan():
    """Renders the planning page."""
    return render_template(
        'plan.html',
        title='Plan',
        year=datetime.now().year,
        message='Your planning page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Rendezvous With Me was created in 36 hours by a team of Rose-Hulman Students.'
    )

@app.route('/schedule/create', methods=['POST'])
def schedule():
    data = request.data
    client = pymongo.MongoClient("mongodb://Boilermake:Boilermake2017@cluster0-shard-00-00-sifbq.mongodb.net:27017,cluster0-shard-00-01-sifbq.mongodb.net:27017,cluster0-shard-00-02-sifbq.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    db = client.time_slots
    for date in range(data['start_date'], data['end_date']):
        for i in range(data["start_time"], data["end_time"], data["duration"]):
            time_slot = {"date":date, "time": i, "duration":data['duration'], "open":1, "email":None}
            db.insert_one(time_slot)
    return render_template('sendSchedule.html', title='Send Schedule', bytearray=datetime.now().year)
