from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    favorites = db.Column(db.String(255), nullable=True)

class Properties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Address = db.Column(db.String(255))
    Status = db.Column(db.String(255))
    ListingPrice = db.Column(db.Float)
    SquareFt = db.Column(db.Integer)
    YearBuilt = db.Column(db.Integer)
    Beds = db.Column(db.Float)
    Baths = db.Column(db.Float)
    DaysOnSite = db.Column(db.Integer)
    Latitude = db.Column(db.String(255))
    Longitude = db.Column(db.String(255))
    URL = db.Column(db.String(255))
    HouseImage = db.Column(db.String(255))
    GoogleMapImage = db.Column(db.String(255))
    
@app.route('/')
def start():
    return redirect(url_for('login'))

def print_login_table():
    logins = Login.query.all()
    print("Login Table:")
    for login in logins:
        print(f"ID: {login.id}, Username: {login.username}, Password: {login.password}, Favorites: {login.favorites}")

@app.route('/login', methods=['GET', 'POST'])
def login():
    print_login_table()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Login.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        
        if not Login.query.filter_by(username=username).first():
            if password1 != password2:
                flash('Passwords are not the same. Please try again.')
                return redirect(url_for('login'))
            hashed_password = generate_password_hash(password1)
            new_user = Login(username=username, password=hashed_password, favorites='')
            db.session.add(new_user)
            db.session.commit()
        else: 
            flash('Username already taken. Please try again.')
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/home')
def home():
    username = session.get('username')

    # Generate an array with 5 random numbers between 1 and the maximum ID in the Properties table
    max_id = db.session.query(db.func.max(Properties.id)).scalar()
    random_id = random.sample(range(1, max_id + 1), 5)

    random_properties = []
    for property_id in random_id:
        property = db.session.get(Properties, property_id)
        if property:
            random_properties.append({
                'ID': property.id,
                'Address': property.Address,
                'Status': property.Status,
                'Listing Price': property.ListingPrice,
                'Square Ft': property.SquareFt,
                'Year Built': property.YearBuilt,
                'Beds': property.Beds,
                'Baths': property.Baths,
                'Days On Site': property.DaysOnSite,
                'Latitude': property.Latitude,
                'Longitude': property.Longitude,
                'URL': property.URL,
                'House Image': property.HouseImage,
                'Google Map Image': property.GoogleMapImage
            })
    
    return render_template('home.html', username=username, random_properties=random_properties)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        # Retrieve form data
        min_price = request.form.get('min_price')
        max_price = request.form.get('max_price')
        beds = request.form.get('beds')
        baths = request.form.get('baths')
        min_year_built = request.form.get('min_year_built')
        max_year_built = request.form.get('max_year_built')
        square_ft = request.form.get('square_ft')
        days_on_site = request.form.get('days_on_site')
        status = request.form.get('status')
        advanceSearch = request.form.get('advanceSearch')

        # Build the query based on the form data
        query = Properties.query
        if min_price:
            query = query.filter(Properties.ListingPrice >= float(min_price))
        if max_price:
            query = query.filter(Properties.ListingPrice <= float(max_price))
        if beds.isdigit():
            query = query.filter(Properties.Beds >= float(beds))
        if baths.isdigit():
            query = query.filter(Properties.Baths >= float(baths))
        if min_year_built:
            query = query.filter(Properties.YearBuilt >= int(min_year_built))
        if max_year_built:
            query = query.filter(Properties.YearBuilt <= int(max_year_built))
        if square_ft.isdigit():
            query = query.filter(Properties.SquareFt >= int(square_ft))
        if days_on_site.isdigit():
            if int(days_on_site) == 12:
                query = query.filter(Properties.DaysOnSite <= 365)
            else:
                query = query.filter(Properties.DaysOnSite <= int(days_on_site * 30))
        if status != 'Any':
            query = query.filter(Properties.Status == status)
        if advanceSearch:
            query = query.filter(Properties.Address.like(f'%{advanceSearch}%'))

        # Execute the query and convert the results to a list of dictionaries
        results = [
            {
                'ID': property.id,
                'Address': property.Address,
                'Status': property.Status,
                'Listing Price': property.ListingPrice,
                'Square Ft': property.SquareFt,
                'Year Built': property.YearBuilt,
                'Beds': property.Beds,
                'Baths': property.Baths,
                'Days On Site': property.DaysOnSite,
                'Latitude': property.Latitude,
                'Longitude': property.Longitude,
                'URL': property.URL,
                'House Image': property.HouseImage,
                'Google Map Image': property.GoogleMapImage
            } for property in query.all()
        ]
        results_count = len(results)
        return render_template('search.html', results=results, results_count=results_count)
    return redirect(url_for('home'))

@app.route('/addToFav', methods=['POST'])
def addToFav():
    if request.method == 'POST':
        # Retrieve the ID of the property from the form data
        property_id = request.form.get('property_id')
        
        # Retrieve the username from the session
        username = session.get('username')
        
        # Find the user in the database
        user = Login.query.filter_by(username=username).first()
        
        if user:
            # Retrieve the existing favorites string or initialize it if it's None
            favorites = user.favorites or ''
            
            # Check if the property ID is already in the favorites
            if property_id not in favorites.split(','):
                # Add the property ID to the favorites string
                if favorites:
                    favorites += ',' + property_id
                else:
                    favorites = property_id
                
                # Update the favorites column in the database
                user.favorites = favorites
                db.session.commit()
                return '', 204  # Success response
            else:
                return '', 204 # Already Exist Change so it makes msg
        else:
            return '', 400  # User not found
        
@app.route('/removeFromFav', methods=['POST'])
def removeFromFav():
    if request.method == 'POST':
        # Retrieve the ID of the property from the form data
        property_id = request.form.get('property_id')
        
        # Retrieve the username from the session
        username = session.get('username')
        
        # Find the user in the database
        user = Login.query.filter_by(username=username).first()
        
        if user:
            # Retrieve the existing favorites string or initialize it if it's None
            favorites = user.favorites or ''
            
            # Split the favorites string into a list of property IDs
            favorite_ids = favorites.split(',') if favorites else []
            
            # Check if the property ID is in the list of favorites
            if property_id in favorite_ids:
                # Remove the property ID from the list of favorites
                favorite_ids.remove(property_id)
                
                # Join the remaining favorite IDs back into a string
                favorites = ','.join(favorite_ids)
                
                # Update the favorites column in the database
                user.favorites = favorites
                db.session.commit()
                
                return redirect(url_for('favorites'))
            else:
                return '', 204 # Not reachable
        else:
            return '', 400  # Not reachable

@app.route('/favorites')
def favorites():
    # Get the username from the session
    username = session.get('username')
    user = Login.query.filter_by(username=username).first()
    if user:
        # Split the favorites string into a list of property IDs
        favorite_ids = [int(id) for id in user.favorites.split(',') if id.isdigit()] if user.favorites else []

        # Query the database to get the details of the favorite properties
        favorite_properties = []
        for property_id in favorite_ids:
            property = db.session.get(Properties, property_id)
            if property:
                favorite_properties.append({
                    'ID': property.id,
                    'Address': property.Address,
                    'Status': property.Status,
                    'Listing Price': property.ListingPrice,
                    'Square Ft': property.SquareFt,
                    'Year Built': property.YearBuilt,
                    'Beds': property.Beds,
                    'Baths': property.Baths,
                    'Days On Site': property.DaysOnSite,
                    'Latitude': property.Latitude,
                    'Longitude': property.Longitude,
                    'URL': property.URL,
                    'House Image': property.HouseImage,
                    'Google Map Image': property.GoogleMapImage
                })
        return render_template('favorites.html', favorite_properties=favorite_properties)
    
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')

@app.route('/changePW', methods=['GET', 'POST'])
def changePW():
    if request.method == 'POST':
        username = session.get('username')
        password1 = request.form['password1']
        password2 = request.form['password2']
        
        user = Login.query.filter_by(username=username).first()

        if password1 != password2:
            flash('Passwords are not the same. Please try again.')
            return redirect(url_for('settings'))
        
        hashed_password = generate_password_hash(password1)
        user.password = hashed_password
        db.session.commit()
        flash("Password Change.")        
    return render_template('settings.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    return render_template('calc.html')

@app.route('/mortgageCalc', methods=['GET', 'POST'])
def mortgageCalc():
    annual_income =  float(request.form.get('annual_income', 0))
    debt_to_income = 0.28
    monthly_payment = annual_income * (debt_to_income / 12.0)
    interest = 0.045
    loan_term = 360
    mortgage_max = monthly_payment * ((1 + interest / 12) ** loan_term - 1) / ((interest / 12) * (1 + interest / 12) ** loan_term)
    return render_template('calc.html', mortgage_max=mortgage_max)

if __name__ == '__main__':
    app.run(debug=True)