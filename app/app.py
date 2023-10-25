from flask import Flask, render_template, redirect, url_for, request
from flask import Blueprint
from blueprints import bug_blueprint

app = Flask(__name__)
#app.register_blueprint(bug_blueprint)   coś tu jest nie tak

def home():
    return "Welcome to the home page!"

if __name__ == "__main__":
    app.run()
