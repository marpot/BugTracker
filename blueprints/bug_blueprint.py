from flask import Blueprint

bug_blueprint = Blueprint('bug', __name__)

@bug_blueprint.route('/list')
def list_bugs():
    return 'List of bugs'

@bug_blueprint.route('/add')
def add_bug():
    return 'Add a new bug'