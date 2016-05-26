from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

class data1(db.Model):
    __tablename__ = 'data1'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    firstNumber = db.Column(db.Integer)
    secondNumber = db.Column(db.Integer)
    thirdNumber = db.Column(db.Integer)
    fourthNumber = db.Column(db.Integer)



    def __init__(self, firstNumber, secondNumber, thirdNumber, fourthNumber):

        self.firstNumber = firstNumber
        self.secondNumber = secondNumber
        self.thirdNumber = thirdNumber
        self.fourthNumber = fourthNumber


db.create_all()


@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(data1).all()
    return render_template('raw.html', data1=fd)


@app.route("/result")
def show_result():
    fd_list = db.session.query(data1).all()

    # Some simple statistics for sample questions
    mean_1 = []
    mean_2 = []
    mean_3 = []
    mean_4 = []


    for el in fd_list:
        mean_1.append(int(el.firstNumber))
    if len(mean_1)> 0:
        mean_sat1 = statistics.mean(mean_1)
    else:
        mean_sat1 = 0

    for el in fd_list:
        mean_2.append(int(el.secondNumber))
    if len(mean_2)> 0:
        mean_sat2 = statistics.mean(mean_2)
    else:
        mean_sat2 = 0

    for el in fd_list:
        mean_3.append(int(el.thirdNumber))
    if len(mean_3)> 0:
        mean_sat3 = statistics.mean(mean_3)
    else:
        mean_sat3 = 0

    for el in fd_list:
        mean_4.append(int(el.fourthNumber))
    if len(mean_4)> 0:
        mean_sat4 = statistics.mean(mean_4)
    else:
        mean_sat4 = 0



    # Prepare data for google charts
    data = [['Pole1', mean_sat1], ['Pole2', mean_sat2], ['Pole3', mean_sat3], ['Pole4', mean_sat4]]

    return render_template('result.html', data=data)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    firstNumber = request.form['firstNumber']
    secondNumber = request.form['secondNumber']
    thirdNumber = request.form['thirdNumber']
    fourthNumber = request.form['fourthNumber']

    # Save the data
    fd = data1(firstNumber, secondNumber, thirdNumber, fourthNumber,)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()