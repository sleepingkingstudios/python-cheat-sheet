from anaconda import application


@application.route('/')
def hello_world():
    return '<p>Greetings, starfighter!</p>'
