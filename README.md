BugTracker Project
Table of Contents
Introduction
System Requirements
Installation
Running the Project
Usage
Configuration
Development
Known Issues
Conclusion
Introduction
BugTracker is a web application designed to manage bug reports within projects. It allows users to create projects, add bug reports, assign them, and track their statuses. This project is built in Python using the Flask framework and SQLAlchemy for database management.

System Requirements
To run and develop BugTracker, you need:

Python 3.x
Flask
Flask-SQLAlchemy
Flask-Login
Flask-WTF
Flask-Migrate
Flask-Bcrypt
SQLite (or another database engine)
Installation
Clone the Repository:


git clone https://github.com/yourusername/BugTracker.git
cd BugTracker
Create and Activate a Virtual Environment (recommended):


python -m venv venv
source venv/bin/activate  # for Unix/Linux
venv\Scripts\activate  # for Windows
Install Dependencies:


pip install -r requirements.txt

Running the Project

Initialize the Database (first run only):
flask db init
flask db migrate
flask db upgrade

Run the Application:
flask run
The app will start at http://localhost:5000.

Usage
After starting the project, log in as an administrator with default credentials:

Username: admin
Password: 321meme321
Once logged in, you can manage projects and bug reports.

Configuration
Configuration options, such as the database and app secret key, can be adjusted in the config.py file.

Development
To further develop this project, you can add new features, fix bugs, or customize it to your needs. This project is built with Flask, making it ideal for easy web app development.

Known Issues
Currently, there are no significant issues. Please report any bugs on the GitHub issues page.

Conclusion
BugTracker is a straightforward and effective tool for managing bug reports in projects. Written in Python and Flask, it is easy to customize and extend.

Thank you for using BugTracker!
