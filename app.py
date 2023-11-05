from flask import Flask, render_template, flash, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import datetime

# Inicjalizacja aplikacji Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugtracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '321meme321'

# Inicjalizacja bazy danych
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

# Inicjalizacja systemu logowania
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Funkcja do wczytywania użytkownika na podstawie ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Klasa reprezentująca projekty w bazie danych
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bugs = db.relationship('Bug', backref='project', lazy=True)

# Klasa reprezentująca zgłoszenia błędów w bazie danych
class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Open')

# Klasa reprezentująca logi zgłoszeń błędów
class BugLog(db.Model):
    __tablename__ = 'bug_log'
    id = db.Column(db.Integer, primary_key=True)
    bug_id = db.Column(db.Integer, db.ForeignKey('bug.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Formularz do tworzenia projektów
class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    submit = SubmitField('Create Project')

# Klasa reprezentująca użytkowników w bazie danych
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    projects = db.relationship('Project', backref='user', lazy=True)
    bugs = db.relationship('Bug', backref='user', lazy=True)

# Inicjalizacja użytkownika "admin" w bazie danych
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if admin is None:
        admin = User(username='admin', password_hash=bcrypt.generate_password_hash('321meme321').decode('utf-8'), role='Admin')
        db.session.add(admin)
        db.session.commit()
        
# Widok dodawania projektu przez administratora
@app.route('/admin/add_project', methods=['GET', 'POST'])
@login_required
def admin_add_project():
    if current_user.role != 'Admin':
        abort(403)  # Odmowa dostępu dla nieadministratorów

    form = ProjectForm()
    if form.validate_on_submit():
        # Sprawdzenie unikalności nazwy projektu
        if Project.query.filter_by(name=form.name.data).first() is not None:
            flash('Projekt o tej nazwie już istnieje.', 'danger')
            return redirect(url_for('admin_add_project'))

        new_project = Project(name=form.name.data, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        flash('Dodano nowy projekt', 'success')
        return redirect(url_for('admin_projects'))
    return render_template('admin/add_project.html', form=form)

# Widok panelu administratora
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'Admin':
        abort(403)  # Odmowa dostępu dla nieadministratorów

    # Dodaj obsługę formularza do dodawania projektów
    project_form = ProjectForm()

    if project_form.validate_on_submit():
        new_project = Project(name=project_form.name.data, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        flash('Dodano nowy projekt', 'success')
        return redirect(url_for('admin'))

    project_form = ProjectForm()
    
    # Tutaj umieść kod wyświetlający panel administratora z formularzem
    return render_template('admin/admin.html', project_form=project_form)


# Widok użytkowników administratora
@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'Admin':
        abort(403)  # Odmowa dostępu dla nieadministratorów
    
    users = User.query.all()  # Pobierz listę użytkowników
    return render_template('admin/users.html', users=users)



# Widok projektów administratora
@app.route('/admin/projects')
@login_required
def admin_projects():
    if current_user.role != 'Admin':
        abort(403)  # Odmowa dostępu dla nieadministratorów
    
    projects = Project.query.all()  # Pobierz listę projektów
    return render_template('admin/projects.html', projects=projects)
# Formularz logowania
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('User', 'User'), ('Admin', 'Admin')], validators=[DataRequired()])

# Formularz rejestracji
class RegistrationForm(FlaskForm):
    new_username = StringField('Username', validators=[DataRequired()])
    new_password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('User', 'User'), ('Admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Create Account')

# Formularz zgłaszania błędu
class BugForm(FlaskForm):
    description = TextAreaField('Bug Description', validators=[DataRequired()])
    project = SelectField('Project', coerce=int)
    status = SelectField('Status', choices=[('Open', 'Open'), ('Closed', 'Closed')], validators=[DataRequired()])
    submit = SubmitField('Add Bug')

# Strona główna
@app.route('/')
def index():
    return render_template('home.html')

# Widok logowania

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Zalogowano pomyślnie', 'success')

            # Przekierowanie do odpowiedniej strony w zależności od roli użytkownika
            if user.role == 'Admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('dashboard'))  # Przekierowanie do panelu użytkownika po zalogowaniu
        else:
            flash('Nieprawidłowa nazwa użytkownika lub hasło', 'danger')

    return render_template('auth/login.html', form=form)


# Widok rejestracji
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')

        existing_user = User.query.filter_by(username=form.new_username.data).first()
        if existing_user is None:
            user = User(username=form.new_username.data, password_hash=hashed_password, role=form.role.data)

            db.session.add(user)
            db.session.commit()

            login_user(user)  # Logowanie użytkownika po rejestracji

            flash('Account created successfully. You are now logged in.', 'success')
            return redirect(url_for('dashboard')) # Przekierowanie do strony logowania po udanej rejestracji
        else:
            flash('Username already exists. Please choose a different username.', 'danger')

    return render_template('register.html', form=form)


# Widok dodawania projektu
@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        new_project = Project(name=form.name.data, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        flash('Dodano nowy projekt', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_project.html', form=form)

# Widok wylogowywania
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_bug', methods=['GET', 'POST'])
@login_required
def add_bug():
    form = BugForm()
    form.project.choices = [(project.id, project.name) for project in Project.query.all()]

    if form.validate_on_submit():
        description = form.description.data
        project_id = form.project.data
        status = form.status.data

        # Pobierz aktualnie zalogowanego użytkownika
        user = current_user

        if user:
            project = Project.query.get(project_id)
            if project:
                new_bug = Bug(description=description, project=project, user=user, status=status)
                db.session.add(new_bug)
                db.session.commit()
                flash('Błąd został dodany pomyślnie', 'success')

                # Przekieruj użytkownika na listę błędów
                return redirect(url_for('dashboard'))
            else:
                flash('Nie znaleziono projektu o takim ID', 'danger')
        else:
            flash('Nieprawidłowy użytkownik', 'danger')

    return render_template('add_bug.html', form=form)

# Widok edycji zgłoszenia błędu
@app.route('/edit_bug/<int:bug_id>', methods=['GET', 'POST'])
@login_required
def edit_bug(bug_id):
    bug = Bug.query.get(bug_id)

    if bug:
        form = BugForm()
        form.project.choices = [(project.id, project.name) for project in Project.query.all()]
        if form.validate_on_submit():
            description = form.description.data
            project_id = form.project.data
            project = Project.query.get(project_id)

            if project:
                bug.description = description
                bug.project = project
                bug.status = form.status.data
                db.session.commit()

                flash('Błąd został zaktualizowany pomyślnie', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Nie znaleziono projektu o takim ID', 'danger')

        form.description.data = bug.description
        form.project.data = bug.project.id
        form.status.data = bug.status

        return render_template('edit_bug.html', form=form, bug=bug)
    else:
        flash('Nie znaleziono błędu o podanym ID', 'danger')
        return redirect(url_for('dashboard'))

# Widok panelu użytkownika
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.id

    if current_user.role == 'Admin':
        user_bugs = Bug.query.all()  # Administratorzy widzą wszystkie zgłoszone błędy
    else:
        user_bugs = Bug.query.filter_by(user_id=user_id).all()  # Zalogowani użytkownicy widzą tylko swoje błędy

    return render_template('dashboard.html', user_bugs=user_bugs)

# Nowy widok, który wyświetla wszystkie zgłoszone błędy, dostępny tylko dla administratorów
@app.route('/admin/all_bugs')
@login_required
def admin_all_bugs():
    if current_user.role != 'Admin':
        abort(403)  # Odmowa dostępu dla nieadministratorów

    all_bugs = Bug.query.all()  # Administratorzy widzą wszystkie zgłoszone błędy

    return render_template('admin/all_bugs.html', all_bugs=all_bugs)


# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)