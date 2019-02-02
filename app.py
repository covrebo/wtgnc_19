from flask import Flask, render_template, url_for

app = Flask(__name__)

# Example data
picks = [
    {
        'week': 1,
        'display_name': 'Chris O.',
        'pick_1': '#18 - Kyle Busch',
        'pick_2': '#48 - Jimmie Johnson',
        'pick_3': '#78 - Martin Truex Jr.',
        'manufacturer': 'Toyota'
    },
    {
        'week': 1,
        'display_name': 'Silver Fox',
        'pick_1': '#18 - Kyle Busch',
        'pick_2': '#48 - Jimmie Johnson',
        'pick_3': '#78 - Martin Truex Jr.',
        'manufacturer': 'Ford'
    },
    {
        'week': 1,
        'display_name': 'Ev-man',
        'pick_1': '#18 - Kyle Busch',
        'pick_2': '#48 - Jimmie Johnson',
        'pick_3': '#78 - Martin Truex Jr.',
        'manufacturer': 'Ford'
    },
    {
        'week': 2,
        'display_name': 'Jodi',
        'pick_1': '#18 - Kyle Busch',
        'pick_2': '#48 - Jimmie Johnson',
        'pick_3': '#78 - Martin Truex Jr.',
        'manufacturer': 'Chevy'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', active='active')

@app.route('/picks-summary')
def picks_summary():
    return render_template('picks.html', title='Pick Summary', picks=picks)


if __name__ == '__main__':
    app.run()
