from flask import Flask, render_template
import requests
import json

app = Flask(__name__)


def chuck_norris_facts():
    r = requests.get('https://api.chucknorris.io/jokes/random')
    if r.status_code == 200:
        r = json.loads(r.text)
        return r['value']
    else:
        return render_template('norris.html')


@app.route('/', methods=['GET', 'POST'])
def chuck():
    return render_template('chuck.html', joke=chuck_norris_facts())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
