from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    favorites = db.Column(db.String, nullable=True)

with app.app_context():
    db.create_all()
    if not Login.query.filter_by(username='admin').first():
        admin_user = Login(username='admin', password='1234', favorites='')
        db.session.add(admin_user)
        db.session.commit()
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Login.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('home', username=username))
        else:
            flash('Invalid username or password. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/home')
def home():
    username = request.args.get('username')
    return render_template('home.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
'''