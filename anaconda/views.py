from flask import render_template
from anaconda import application


@application.route('/')
def index():
    return render_template('index.html');
