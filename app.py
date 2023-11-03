from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugtracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '321meme321'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bugs = db.relationship('Bug', backref='project', lazy=True)

class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Open')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    new_username = StringField('Username', validators=[DataRequired()])
    new_password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('User', 'User'), ('Admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Create Account')

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    submit = SubmitField('Create Project')

class BugForm(FlaskForm):
    description = TextAreaField('Bug Description', validators=[DataRequired()])
    project = SelectField('Project', coerce=int)
    submit = SubmitField('Add Bug')

@app.route('/')
def index():
    return render_template('home.html')

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
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Nieprawidłowa nazwa użytkownika lub hasło', 'danger')

    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Wygenerowanie hasha dla hasłas
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')

        # Sprawdzenie, czy użytkownik o danej nazwie użytkownika już istnieje
        existing_user = User.query.filter_by(username=form.new_username.data).first()
        if existing_user is None:
            # Tworzenie nowego użytkownika i zapis do bazy danych
            user = User(username=form.new_username.data, password_hash=hashed_password, role=form.role.data)
            db.session.add(user)
            db.session.commit()

            # Logowanie nowego użytkownika po rejestracji
            login_user(user)

            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different username.', 'danger')

    return render_template('register.html', form=form)


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
        project = Project.query.get(project_id)

        if project:
            user = User.query.get(current_user.id)
            new_bug = Bug(description=description, project=project, user=user)
            db.session.add(new_bug)
            db.session.commit()
            flash('Błąd został dodany pomyślnie', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nie znaleziono projektu o takim ID', 'danger')

    return render_template('add_bug.html', form=form)

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
                db.session.commit()

                flash('Błąd został zaktualizowany pomyślnie', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Nie znaleziono projektu o takim ID', 'danger')

        form.description.data = bug.description
        form.project.data = bug.project.id

        return render_template('edit_bug.html', form=form, bug=bug)
    else:
        flash('Nie znaleziono błędu o podanym ID', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.id
    user_bugs = Bug.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', user_bugs=user_bugs)

if __name__ == '__main__':
    app.run(debug=True)
