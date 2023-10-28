from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import hashlib

app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Update with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.static_url_path = '/static'
app.secret_key = '321meme321'  # Set a secret key

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


# Store `hashed_password` in the database

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

def hash_password(password):
    # Generate a salt (you can use a random value)
    salt = "your_salt_value"
    
    # Combine the password and salt and hash it using SHA-256
    hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    
    return hashed_password

password = "user_password"  # The plain text password
hashed_password = hash_password(password)

# Store `hashed_password` in the database

def check_password(input_password, stored_password):
    # Hash the input password using the same method
    hashed_input_password = hash_password(input_password)
    
    # Compare the stored hashed password with the hashed input password
    return hashed_input_password == stored_password

input_password = "user_input_password"  # The plain text password entered during login
stored_password = "retrieved_hashed_password"  # The stored hashed password from the database


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/profile")
@login_required  # Use this decorator to protect routes that require authentication
def profile():
    return render_template('profile.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and user.password == password:
#             login_user(user)
#             return redirect(url_for('profile'))
#         else:
#             return "Login failed"  # You can render a login error template here
#     else:
#         return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        input_password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password(input_password, user.password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            return "Login failed"  # You can render a login error template here
    else:
        return render_template('login.html')


@app.route("/logout")
@login_required  # Use this decorator to protect routes that require authentication
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password before storing it in the database
        hashed_password = hash_password(password)

        # Create a new user and add it to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the login page after successful signup
        return redirect(url_for('login'))
    
    return render_template('signup.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
