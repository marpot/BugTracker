from flask import render_template, flash, redirect, url_for
from flask_login import login_user
from app_v2.app.models import User
from app_v2.app.forms import RegistrationForm
from app_v2.app import db

# ... inne importy ...

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            # Tworzenie nowego użytkownika
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Zarejestrowano pomyślnie', 'success')
            
            # Logowanie nowo utworzonego użytkownika
            login_user(user)

            return redirect(url_for('auth.login'))  # Przekieruj do panelu logowania
        else:
            flash('Nazwa użytkownika jest już zajęta', 'danger')
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Zalogowano pomyślnie', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.user_dashboard'))  # Przekieruj do panelu użytkownika
        else:
            flash('Nieprawidłowa nazwa użytkownika lub hasło', 'danger')

    return render_template('auth/login.html', form=form)
