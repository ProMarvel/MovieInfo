from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'marvelous'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        searchText = request.form['searchText']

        try:
            movies = getMovies(searchText)
        except requests.exceptions.ConnectionError:
            return 'Connection Error, try again.'

        return render_template('home.html', movies=movies)

    return render_template('home.html')

def getMovies(searchText):
    params = {
        's': searchText,
        'apikey': 'd773aa4'
    }

    response = requests.get('http://www.omdbapi.com/', params = params)
    data = response.json()['Search']

    return data

@app.route('/movie/<imdbID>', methods=['GET', 'POST'])
def movieInfo(imdbID):

    params = {
        'i': imdbID,
        'apikey': 'd773aa4'
    }

    response = requests.get('http://www.omdbapi.com/', params = params)
    data = response.json()
    pprint.pprint(data)
    return render_template('movieInfo.html', movie=data)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404