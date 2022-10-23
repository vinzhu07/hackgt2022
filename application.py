# filename: application.py
from queue import Empty
from flask import Flask, render_template, redirect, request, session
import pymysql
from flask_bcrypt import Bcrypt
import bcrypt
from datetime import datetime
from pytz import timezone

application = Flask(__name__) # This needs to be named `application`
application.secret_key = 'any random string'


def get_database_connection():
    conn = pymysql.connect(host='buzzdash.cprggzpyeevc.us-east-1.rds.amazonaws.com',
                             user='root',
                             password='hackgt10-21-22',
                             db='buzzdash',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return conn

conn=get_database_connection()
cursor = conn.cursor()



@application.route("/")
def index():
    if ('username' in session):
        print("You are logged in")
    return render_template('index.html')


@application.route("/login", methods = ['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        print("Logging in")
        statement = f'''SELECT * FROM buzzdash.User WHERE username = "{username}";'''
        cursor.execute(statement)
        result = cursor.fetchall()
        if result is not None:
            if bcrypt.checkpw(password.encode('utf-8'), (result[0]['password'][2:-1]).encode('utf-8')):
                print("Logged in")
                session['username'] = username
                return redirect('/')



@application.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        password = request.form['password']
        password1 = request.form['password1']
        print("HI")
        print(password)
        print(password)
        print(password==password1)
        if(password == password1):
            pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            print("Inserting")
            statement = f'''INSERT INTO buzzdash.User (name, username, email, password, phoneNumber) VALUES ("{name}", "{username}", "{email}", "{pw_hash}", "{str(number)}");'''
            print(statement)
            cursor.execute(statement)  
            conn.commit()
            print("Inserted")
            return redirect('/login')



@application.route("/buyRequest", methods=['GET', 'POST'])
def buy_request():
    if ('username' in session):
        print("You are logged in")
    else: 
        return redirect('/login')
    if request.method == 'GET':
        return render_template('buyRequest.html')
    else:
        print(request.form)
        date = request.form['date']
        time = request.form['time']
        time1 = request.form['time1']
        fundChoice = request.form['fundChoice']
        cost = request.form['cost']
        location = request.form['location']
        offer = request.form['offer']
        extra = request.form['text']
        if (date is not None and time is not None and fundChoice is not None and offer is not None):
            print("Inserting order")
            statement = f'''INSERT INTO buzzdash.Request (username, date, startTime, endTime, funds, location, cost, offer, extra) VALUES ("{session['username']}", "{date}", "{time}", "{time1}", "{fundChoice}", "{location}", "{cost}", "{offer}", "{extra}");'''
            cursor.execute(statement)  
            conn.commit()
            print("Inserted")
            return redirect("/")

@application.route("/sellRequest", methods=['GET', 'POST'])
def sell_request():
    if ('username' in session):
        print("You are logged in")
    else: 
        return redirect('/login')
    if request.method == 'GET':
        return render_template('sellRequest.html')
    else:
        print(request.form)
        date = request.form['date']
        date1 = request.form['date1']
        time = request.form['time']
        time1 = request.form['time1']
        fundChoice = request.form['fundChoice']
        cost = request.form['cost']
        location = request.form['location']
        offer = request.form['offer']
        extra = request.form['text']
        if (date is not None and time is not None and fundChoice is not None and offer is not None):
            print("Inserting offer")
            statement = f'''INSERT INTO buzzdash.Offer (username, startDate, endDate, startTime, endTime, funds, location, cost, offer, extra) VALUES ("{session['username']}", "{date}", "{date1}", "{time}", "{time1}", "{fundChoice}", "{location}", "{cost}", "{offer}", "{extra}");'''
            cursor.execute(statement)  
            conn.commit()
            print("Inserted")
            return redirect("/")

@application.route("/dashboard")
def dashboard_page():
    if ('username' in session):
        print("You are logged in")
    else: 
        return redirect('/login')

    cursor.execute("SELECT * FROM buzzdash.Request WHERE accepted = false ORDER BY date, startTime limit 5;")
    results = cursor.fetchall()
    requests=[]
    for item in results:
        request={}

        request['username'] = item['username']
        request['date'] = str(datetime.strptime(str(item['date']), "%Y-%m-%d").strftime('%b %d'))
        request['startTime'] = str(datetime.strptime(str(item['startTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        request['endTime'] = str(datetime.strptime(str(item['endTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        request['funds'] = item['funds']
        request['location'] = item['location']
        request['cost'] = int(item['cost'])
        request['offer'] = item['offer']
        request['extra'] = item['extra']
        request['requestId'] = item['requestId']
        print(request)

        requests.append(request)

    cursor.execute("SELECT * FROM buzzdash.Offer  ORDER BY startDate, startTime limit 5;")
    results = cursor.fetchall()
    offers=[]
    for item in results:
        request={}
        request['username'] = item['username']
        request['date'] = str(datetime.strptime(str(item['startDate']), "%Y-%m-%d").date().strftime('%b %d'))
        request['date1'] = str(datetime.strptime(str(item['endDate']), "%Y-%m-%d").date().strftime('%b %d'))
        request['startTime'] = str(datetime.strptime(str(item['startTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        request['endTime'] = str(datetime.strptime(str(item['endTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        request['funds'] = item['funds']
        request['location'] = item['location']
        request['cost'] = int(item['cost'])
        request['offer'] = item['offer']
        request['extra'] = item['extra']
        request['offerId'] = item['offerId']
        print(request)

        offers.append(request)
    return render_template('dashboard.html', requests = requests, offers = offers)


@application.route('/request/<string:requestId>', methods=['GET'])
def view_request(requestId):
    if ('username' in session):
        print("You are logged in")
    else: 
        return redirect('/login')
    cursor.execute(f'''SELECT * FROM buzzdash.Request INNER JOIN User ON User.username = Request.username WHERE requestId = {requestId};''')
    result = cursor.fetchall()
    for item in result:
        request={}
        request['username'] = item['username']
        request['date'] = str(datetime.strptime(str(item['date']), "%Y-%m-%d").strftime('%b %d'))
        request['startTime'] = str(datetime.strptime(str(item['startTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        request['endTime'] = str(datetime.strptime(str(item['endTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        request['funds'] = item['funds']
        request['location'] = item['location']
        request['cost'] = int(item['cost'])
        request['offer'] = item['offer']
        request['extra'] = item['extra']
        request['requestId'] = item['requestId']

        cursor.execute(f'''SELECT * FROM buzzdash.AcceptedRequest WHERE requestId = "{requestId}";''')
        result1 = cursor.fetchall()
        if len(result1)>0 and result1[0]['username'] == session['username']:
            request['email'] = item['email']
            request['phoneNumber'] = item['phoneNumber']

        print(request)
    return render_template('viewRequest.html', request = request)

@application.route('/accept/<string:requestId>', methods = ['POST'])
def accept_request(requestId):
    statement = f'''INSERT INTO buzzdash.AcceptedRequest (username, requestId) VALUES ("{session['username']}", "{requestId}");'''
    cursor.execute(statement)  
    conn.commit()
    statement = f'''UPDATE buzzdash.Request set accepted = true WHERE requestId = {requestId};'''
    statement = f'''SELECT * FROM buzzdash.Request INNER JOIN User ON User.username = Request.username WHERE requestId = {requestId};'''
    cursor.execute(statement)
    result = cursor.fetchall()
    for item in result:
        request={}
        request['username'] = item['User.username']
        request['date'] = str(datetime.strptime(str(item['date']), "%Y-%m-%d").strftime('%b %d'))
        request['startTime'] = str(datetime.strptime(str(item['startTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        request['endTime'] = str(datetime.strptime(str(item['endTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        request['funds'] = item['funds']
        request['location'] = item['location']
        request['cost'] = int(item['cost'])
        request['offer'] = item['offer']
        request['extra'] = item['extra']
        request['requestId'] = item['requestId']
        request['email'] = item['email']
        request['phoneNumber'] = item['phoneNumber']

        request['text'] = "Thanks for accepting this request! Here is their phone number and email to contact them."
        return render_template('viewRequest.html', request = request)
    


@application.route('/offer/<string:offerId>', methods=['GET'])
def view_offer(offerId):    
    if ('username' in session):
        print("You are logged in")
    else: 
        return redirect('/login')
    cursor.execute(f'''SELECT * FROM buzzdash.Offer INNER JOIN User ON User.username = Offer.username WHERE offerId = "{offerId}";''')
    result = cursor.fetchall()
    for item in result:
        offer={}
        
        offer['username'] = item['username']
        offer['startDate'] = str(datetime.strptime(str(item['startDate']), "%Y-%m-%d").strftime('%b %d'))
        offer['endDate'] = str(datetime.strptime(str(item['endDate']), "%Y-%m-%d").strftime('%b %d'))
        offer['startTime'] = str(datetime.strptime(str(item['startTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        offer['endTime'] = str(datetime.strptime(str(item['endTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        offer['funds'] = item['funds']
        offer['location'] = item['location']
        offer['cost'] = int(item['cost'])
        offer['offer'] = item['offer']
        offer['extra'] = item['extra']
        offer['offerId'] = item['offerId']
        
        cursor.execute(f'''SELECT * FROM buzzdash.OfferInterest WHERE offerId = "{offerId}";''')
        result1 = cursor.fetchall()
        print(len(result1))
        if len(result1) > 0 and result1[0]['username'] == session['username']:
            offer['email'] = item['email']
            offer['phoneNumber'] = item['phoneNumber']

        print(offer)
    return render_template('viewOffer.html', offer = offer)

@application.route('/interested/<string:offerId>', methods = ['POST'])
def offer_interest(offerId):
    statement = f'''INSERT INTO buzzdash.OfferInterest (username, offerId) VALUES ("{session['username']}", "{offerId}");'''
    cursor.execute(statement)  
    conn.commit()
    statement = f'''SELECT * FROM buzzdash.Offer INNER JOIN User ON User.username = Offer.username WHERE offerId = {offerId};'''
    cursor.execute(statement)
    result = cursor.fetchall()
    for item in result:
        offer={}
        offer['username'] = item['username']
        offer['startDate'] = str(datetime.strptime(str(item['startDate']), "%Y-%m-%d").strftime('%b %d'))
        offer['endDate'] = str(datetime.strptime(str(item['endDate']), "%Y-%m-%d").strftime('%b %d'))
        offer['startTime'] = str(datetime.strptime(str(item['startTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        offer['endTime'] = str(datetime.strptime(str(item['endTime']), "%H:%M:%S").time().strftime('%I:%M %p'))
        offer['funds'] = item['funds']
        offer['location'] = item['location']
        offer['cost'] = int(item['cost'])
        offer['offer'] = item['offer']
        offer['extra'] = item['extra']
        offer['offerId'] = item['offerId']
        offer['email'] = item['email']
        offer['phoneNumber'] = item['phoneNumber']

        offer['text'] = "Thanks for inquiring about this offer! Here is their phone number and email to contact them."
    return render_template('viewOffer.html', offer = offer)


@application.route('/logout', methods=['GET', 'POST'])
def logout():
    print("Logging out")
    session.pop('username')
    return redirect('/') 

@application.route('/about', methods=['GET'])
def about():
    return render_template("about.html")

if __name__ == "__main__":
    application.run(debug=True)