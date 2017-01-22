"""
Routes and views for the flask application.
"""
import datetime
from datetime import datetime as dt
from flask import render_template
from flask import request
from Rendezvous import app
import pymongo
import json

class TimeSlot:
    date=dt.now().day
    time=dt.now().time
    duration=15
    open=1
    email=None
    def __init__(self, date, time, duration, open, email):
        self.date = date
        self.time = time
        self.duration = duration
        self.open = open
        self.email = email

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=dt.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=dt.now().year,
        message='If you have any issues while using Rendezvous With Me - contact us at:'
    )

@app.route('/plan')
def plan():
    """Renders the planning page."""
    return render_template(
        'plan.html',
        title='Plan',
        year=dt.now().year,
        message='Your planning page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=dt.now().year,
        message='Rendezvous With Me was created in 36 hours by a team of Rose-Hulman Students.'
    )

@app.route('/schedule/<schedule_num>/timesluts', methods=['GET'])
def timeslots(schedule_num):    
    client = pymongo.MongoClient("mongodb://Boilermake:Boilermake2017@cluster0-shard-00-00-sifbq.mongodb.net:27017,cluster0-shard-00-01-sifbq.mongodb.net:27017,cluster0-shard-00-02-sifbq.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    schedule = []
    for i in range(0, 10):
        schedule.append({"date":dt.today(), "time": dt.utcnow()+datetime.timedelta(minutes=i), "duration":1,"open":1, "email":None})
    return render_template('timeslot.html', title="Register For Timeslut", year = dt.now().year, items = schedule)

@app.route('/schedule/create', methods=['POST'])
def schedule():
    data = request.form
    client = pymongo.MongoClient("mongodb://Boilermake:Boilermake2017@cluster0-shard-00-00-sifbq.mongodb.net:27017,cluster0-shard-00-01-sifbq.mongodb.net:27017,cluster0-shard-00-02-sifbq.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    db = client.rendezvous
    base = dt.today()
    
    for date in daterange(dt.strptime(data['start_date'], "%m/%d/%Y"),dt.strptime(data['end_date'], "%m/%d/%Y")):
        start = dt.strptime(data["start_time"], "%H:%M")
        end = dt.strptime(data["end_time"], "%H:%M")
        while start <= end:
            time_slot = TimeSlot(str(date), str(start), data['slot_duration'], 1, None)
            db.time_slots.insert_many(time_slot).inserted_id
            start+=datetime.timedelta(minutes=int(data['slot_duration']))

    schedule_num = db.schedule.insert_one(schedule).inserted_id
    return render_template('sendSchedule.html', title='Send Schedule', year=datetime.now().year, schedule_num = schedule_num)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
